#!/usr/bin/env python3
# Restore counterpart of redis_backup.py: SELECT db; RESTORE key ttl dump REPLACE (pipelined).
# Usage: python redis_restore.py <host> <port> <password|-> <backup.jsonl>
import socket, base64, json, time, sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 6379
PASSWORD = sys.argv[3] if len(sys.argv) > 3 else "-"
INP = sys.argv[4] if len(sys.argv) > 4 else "redis-backup.jsonl"

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
    rows = [json.loads(l) for l in open(INP, encoding="utf-8")]
    bydb = {}
    for row in rows:
        bydb.setdefault(row["db"], []).append(row)
    t0 = time.time()
    for db, items in sorted(bydb.items()):
        r.cmd("SELECT", db)
        ok = fail = 0
        B = 200
        for i in range(0, len(items), B):
            chunk = items[i:i + B]
            cmds = [("RESTORE", base64.b64decode(it["key"]), it["ttl"],
                     base64.b64decode(it["dump"]), "REPLACE") for it in chunk]
            for res in r.pipe(cmds):
                if res == "OK":
                    ok += 1
                else:
                    fail += 1
        print(f"db{db}: restored={ok} failed={fail}", flush=True)
    print("verify keyspace:", flush=True)
    for db in sorted(bydb):
        r.cmd("SELECT", db)
        print(f"db{db}: dbsize={r.cmd('DBSIZE')}", flush=True)
    print(f"done in {time.time() - t0:.1f}s", flush=True)

if __name__ == "__main__":
    main()
