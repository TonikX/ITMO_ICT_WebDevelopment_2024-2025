import socket
import threading


class ChatServer:
    def __init__(self, host="127.0.0.1", port=4000, max_connections=10):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(max_connections)
        self.users = {}

    def broadcast(self, sender_conn, message):
        for conn, name in self.users.items():
            if conn != sender_conn:
                try:
                    conn.send(f'{self.users[sender_conn]}: {message}'.encode())
                except Exception as e:
                    print(f"Error sending message to {name}: {e}")
                    conn.close()
                    self.remove_user(conn)

    def remove_user(self, conn):
        if conn in self.users:
            print(f"User {self.users[conn]} disconnected.")
            del self.users[conn]

    def handle_client(self, conn):
        try:
            while True:
                msg = conn.recv(1024).decode()
                if not msg or msg.lower() == 'quit':
                    self.remove_user(conn)
                    break
                self.broadcast(conn, msg)
        except ConnectionResetError:
            self.remove_user(conn)
        finally:
            conn.close()

    def start(self):
        print("Server started. Waiting for connections...")
        while True:
            conn, addr = self.server.accept()
            print(f"New connection from {addr}")
            name = conn.recv(1024).decode()
            self.users[conn] = name
            print(f"User {name} connected.")
            client_thread = threading.Thread(target=self.handle_client, args=(conn,))
            client_thread.start()


chat_server = ChatServer()
chat_server.start()
