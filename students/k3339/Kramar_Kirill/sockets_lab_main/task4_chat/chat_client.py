from __future__ import annotations
import socket, threading, sys

HOST = "127.0.0.1"
PORT = 6000

def recv_loop(sock: socket.socket) -> None:
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[Disconnected]")
                break
            sys.stdout.write(data.decode("utf-8", errors="replace"))
            sys.stdout.flush()
    except OSError:
        pass

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        t = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
        t.start()
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                sock.sendall(line.encode("utf-8"))
                if line.strip() == "/quit":
                    break
        finally:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

if __name__ == "__main__":
    main()
