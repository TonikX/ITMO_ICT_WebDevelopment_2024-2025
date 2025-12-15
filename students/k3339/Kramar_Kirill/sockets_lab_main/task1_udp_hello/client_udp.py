from __future__ import annotations
import socket

HOST = "127.0.0.1"
PORT = 9999

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(b"Hello, server", (HOST, PORT))
        sock.settimeout(3.0)
        data, _ = sock.recvfrom(4096)
        print("Server replied:", data.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()
