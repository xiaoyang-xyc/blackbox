#!/usr/bin/env python3
# Full logical backup of a Redis instance (all 16 DBs) via raw RESP protocol.
# Pipelined DUMP + PTTL per key -> JSONL. Read-only, safe for production.
# Usage: python redis_backup.py <host> <port> <password|-> <out.jsonl>
import socket, base64, json, time, sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 6379
PASSWORD = sys.argv[3] if len(sys.argv) > 3 else "-"
OUT = sys.argv[4] if len(sys.argv) > 4 else "redis-backup.jsonl"

class R:
    def __init__(self, host, port, password):
        self.s = socket.create_connection((host, port), timeout=60)
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.f = self.s.makefile("rb")
        if password and password != "-":
            r = self.cmd("AUTH", password)
            assert r == "OK", r
    def _read(self):
        line = self.f.readline()
        if not line:
            raise ConnectionError("eof")
        t, rest = line[:1], line[1:-2]
        if t == b"+":
            return rest.decode("utf-8", "replace")
        if t == b"-":
            raise RuntimeError(rest.decode("utf-8", "replace"))
        if t == b":":
            return int(rest)
        if t == b"$":
            n = int(rest)
            if n < 0:
                return None
            d = self.f.read(n)
            self.f.read(2)
            return d
        if t == b"*":
            n = int(rest)
            if n < 0:
                return None
            return [self._read() for _ in range(n)]
        raise RuntimeError("bad reply: %r" % line[:60])
    @staticmethod
    def _enc(cmds):
        d = b""
        for args in cmds:
            d += ("*%d\r\n" % len(args)).encode()
            for a in args:
                if not isinstance(a, bytes):
                    a = str(a).encode()
                d += ("$%d\r\n" % len(a)).encode() + a + b"\r\n"
        return d
    def cmd(self, *args):
        self.s.sendall(self._enc([args]))
        return self._read()
    def pipe(self, cmds):
        self.s.sendall(self._enc(cmds))
        out = []
        for _ in cmds:
            try:
                out.append(self._read())
            except Exception as e:
                out.append(e)
        return out

def main():
    r = R(HOST, PORT, PASSWORD)
    total, t0 = 0, time.time()
    with open(OUT, "w", encoding="utf-8") as out:
        for db in range(16):
            try:
                r.cmd("SELECT", db)
            except Exception as e:
                print(f"db{db}: SELECT failed: {e}", flush=True)
                continue
            n = r.cmd("DBSIZE")
            if not n:
                continue
            cursor, keys = 0, []
            while True:
                cursor, batch = r.cmd("SCAN", cursor, "COUNT", 1000)
                keys.extend(batch)
                if int(cursor) == 0:
                    break
            got = 0
            B = 200
            for i in range(0, len(keys), B):
                chunk = keys[i:i + B]
                reqs = []
                for k in chunk:
                    reqs.append(("PTTL", k))
                    reqs.append(("DUMP", k))
                res = r.pipe(reqs)
                for j, k in enumerate(chunk):
                    ttl, dump = res[2 * j], res[2 * j + 1]
                    if not isinstance(dump, (bytes, type(None))) or dump is None:
                        continue
                    out.write(json.dumps({
                        "db": db,
                        "key": base64.b64encode(k).decode(),
                        "ttl": ttl if (isinstance(ttl, int) and ttl > 0) else 0,
                        "dump": base64.b64encode(dump).decode(),
                    }) + "\n")
                    got += 1
            total += got
            print(f"db{db}: dbsize={n} backed_up={got}", flush=True)
    print(f"TOTAL {total} keys in {time.time() - t0:.1f}s -> {OUT}", flush=True)

if __name__ == "__main__":
    main()
