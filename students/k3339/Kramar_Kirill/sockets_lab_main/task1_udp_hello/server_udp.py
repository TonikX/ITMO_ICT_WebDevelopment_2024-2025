from __future__ import annotations
import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 9999

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"[{datetime.now():%H:%M:%S}] UDP server listening on {HOST}:{PORT}")
        while True:
            data, addr = sock.recvfrom(4096)
            text = data.decode("utf-8", errors="replace")
            print(f"[{datetime.now():%H:%M:%S}] from {addr}: {text!r}")
            sock.sendto(b"Hello, client", addr)

if __name__ == "__main__":
    main()
