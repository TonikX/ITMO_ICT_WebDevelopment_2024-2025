from __future__ import annotations
import socket, threading
from typing import Dict, Tuple, List

HOST = "127.0.0.1"
PORT = 6000

clients_lock = threading.Lock()
clients: Dict[socket.socket, Tuple[str, Tuple[str, int]]] = {}

def broadcast(sender_sock: socket.socket, message: str) -> None:
    dead: List[socket.socket] = []
    with clients_lock:
        for sock, (nick, addr) in list(clients.items()):
            if sock is sender_sock:
                continue
            try:
                sock.sendall(message.encode("utf-8"))
            except OSError:
                dead.append(sock)
        for d in dead:
            clients.pop(d, None)

def handle_client(conn: socket.socket, addr) -> None:
    with conn:
        conn.sendall(b"Enter your nickname: ")
        nick = conn.recv(1024).decode("utf-8", errors="replace").strip() or f"{addr[0]}:{addr[1]}"
        with clients_lock:
            clients[conn] = (nick, addr)
        join_msg = f"* {nick} joined from {addr}\n"
        print(join_msg.strip())
        broadcast(conn, join_msg)
        try:
            conn.sendall(b"Type messages, /quit to exit\n")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                text = data.decode("utf-8", errors="replace")
                if text.strip() == "/quit":
                    break
                broadcast(conn, f"[{nick}] {text}")
        finally:
            with clients_lock:
                clients.pop(conn, None)
            leave_msg = f"* {nick} left\n"
            print(leave_msg.strip())
            broadcast(conn, leave_msg)

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"Chat server on {HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
