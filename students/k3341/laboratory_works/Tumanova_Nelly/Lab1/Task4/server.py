import socket
import threading

class ChatServer:
    HOST = "localhost"
    PORT = 9090
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # чтобы сразу после перезапуска сервера заново привязать его к тому же порту без ошибки
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clients = {}
        self.clients_lock = threading.Lock()

    def start(self):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(socket.SOMAXCONN)
        print(f"[*] TCP-server started on {self.HOST}:{self.PORT}")

        while True:
            client_sock, client_addr = self.sock.accept()
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_sock, client_addr), daemon=True
            )
            client_thread.start()

    def handle_client(self, client_sock, client_addr):
        was_added = False
        username = None
        try:
            print(f"[+] {client_addr[0]}:{client_addr[1]} connected.")
            client_sock.sendall("Enter your name: ".encode('utf-8'))
            username = client_sock.recv(1024).decode('utf-8').strip()

            if not username:
                client_sock.sendall("[x] Incorrect name.".encode('utf-8'))
                return

            if not self.try_add_client(username, client_sock):
                client_sock.sendall("[x] This name is already taken.".encode('utf-8'))
                return

            was_added = True
            self.print_members()
            while True:
                data = client_sock.recv(1024)
                if not data: break
                text = data.decode('utf-8').strip()
                full_message = f"[{username}] {text}"
                print(full_message)
                self.broadcast(full_message, exclude=client_sock)
        except OSError:
            pass
        finally:
            if was_added: self.remove_clients([username])
            self.print_members()
            client_sock.close()
            print(f"[-] {client_addr[0]}:{client_addr[1]} disconnected.")

    def try_add_client(self, username, client_sock):
        with self.clients_lock:
            if username in self.clients:
                return False
            self.clients[username] = client_sock

        print(f"[!] {username} joined the chat.")
        self.broadcast(f"*** {username} joined the chat! ***")
        return True

    def remove_clients(self, usernames):
        with self.clients_lock:
            for username in usernames:
                self.clients.pop(username, None)

        for username in usernames:
            print(f"[!] {username} left the chat.")
            self.broadcast(f"*** {username} left the chat! ***")

    def broadcast(self, message, exclude=None):
        with self.clients_lock:
            targets = [(name, sock) for name, sock in self.clients.items() if sock is not exclude]

        for username, sock in targets:
            try: sock.sendall(message.encode('utf-8'))
            except OSError: return

    def stop(self):
        with self.clients_lock:
            for client_sock in self.clients.values():
                try:
                    client_sock.close()
                except OSError:
                    pass
        self.sock.close()

    def print_members(self):
        print("[*] Members:", end=" ")
        print(*self.clients.keys(), sep=", ")


if __name__ == "__main__":
    server = ChatServer()
    try: server.start()
    except KeyboardInterrupt: pass
    finally: server.stop()
