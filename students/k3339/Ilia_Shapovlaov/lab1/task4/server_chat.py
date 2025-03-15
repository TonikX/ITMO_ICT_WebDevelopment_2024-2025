import threading
import socket
import sys


class ServerChat:
    def __init__(
        self, host="localhost", port=8080, backlog: int | None = None
    ) -> None:
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host, port))

        if backlog is None:
            self._socket.listen()
        else:
            self._socket.listen(backlog)

        self._clients = {}

    def _broadcast(self, message: str, sender_name: str) -> None:
        for name, conn in self._clients.items():
            if name != sender_name:
                try:
                    conn.sendall(message.encode())
                except Exception as e:
                    print(f"Failed to send message to {name}: {e}")
                    self._clients.pop(name)

    def _handle_client(self, conn: socket, addr) -> None:
        print(f"New connection: {addr}")

        try:
            conn.send("Enter your name: ".encode())
            name = conn.recv(1024).decode()
            self._clients[name] = conn

            conn.send(f"Welcome to the chat, {name}!".encode())
            print(f"{name} has joined the chat")

            while True:
                message = conn.recv(1024).decode()
                if not message:
                    break
                print(f"Received from {name}: {message}")

                broadcast_message = f"{name}: {message}"
                self._broadcast(broadcast_message, name)

        except Exception as e:
            print(f"Error handling client {addr}: {e}", sys.stderr)

        finally:
            print(f"Client {name} disconnected")

            self._clients.pop(name, None)
            conn.close()

    def run(self):
        print(f"Server started at {self._host}:{self._port}")

        while True:
            conn, addr = self._socket.accept()

            thread = threading.Thread(
                target=self._handle_client, args=(conn, addr)
            )
            thread.start()


server = ServerChat()
server.run()
