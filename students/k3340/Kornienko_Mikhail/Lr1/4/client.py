import socket
import threading
import time

class ChatClient:
    def __init__(self, ip="127.0.0.1", port=4000, name="Client"):
        self.server_ip = ip
        self.server_port = port
        self.name = name
        self.buffer_size = 1024
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.connection.connect((self.server_ip, self.server_port))
            self.connection.send(self.name.encode())
            print(f"Connected to server at {self.server_ip}:{self.server_port} as {self.name}")
        except ConnectionError as e:
            print(f"Failed to connect: {e}")
            return False
        return True

    def receive_messages(self):
        while True:
            try:
                message = self.connection.recv(self.buffer_size).decode()
                if message:
                    print(message)
                else:
                    print("Connection closed by the server.")
                    self.connection.close()
                    break
            except ConnectionError as e:
                print(f"Error receiving message: {e}")
                break

    def send_messages(self):
        while True:
            try:
                message = f"Hello {time.time()}"
                self.connection.send(message.encode())
                time.sleep(2)
            except ConnectionError as e:
                print(f"Error sending message: {e}")
                break

    def start(self):
        if self.connect_to_server():
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.send_messages()
