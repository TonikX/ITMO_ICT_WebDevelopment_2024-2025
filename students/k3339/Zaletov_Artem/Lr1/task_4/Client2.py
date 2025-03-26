import socket
import threading

class Client:
    def __init__(self, ip, port, encoding="utf-8", buffer_size=1024):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        print("Connected to the server")

        self.encoding = encoding
        self.buffer_size = buffer_size

        self.receive_thread = threading.Thread(target=self.receive_thread_method)
        self.receive_thread.start()

        self.send_thread = threading.Thread(target=self.send_thread_method)
        self.send_thread.start()

    def disconnect(self):
        self.running = False
        self.sock.close()
        print("Disconnected from the server")

    def send_message(self, message: str):
        self.sock.sendall(message.encode(self.encoding))

    def receive_thread_method(self):
        print("Started receiving the messages from the server")
        while self.running:
            try:
                message = self.sock.recv(self.buffer_size).decode(self.encoding)
                print(message)
            except:
                self.disconnect()
                break

    def send_thread_method(self):
        while self.running:
            self.send_message(input())

if __name__ == "__main__":
    server_addr = "localhost"
    server_port = 8080
    Client(server_addr, server_port)
