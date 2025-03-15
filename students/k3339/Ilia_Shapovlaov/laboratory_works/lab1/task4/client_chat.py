import threading
import socket
import sys


class ClientChat:
    def __init__(self, server_host="localhost", server_port=8080):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((server_host, server_port))

    def send(self):
        while True:
            message = input()
            if message:
                print(f"Sending message to server: {message}")
                self._socket.send(message.encode())

    def receive(self):
        while True:
            try:
                message = self._socket.recv(1024).decode()
                if message:
                    print(message)

            except:
                print("Lost connection to server", sys.stderr)
                break

    def run(self) -> None:
        receive_thread = threading.Thread(target=self.receive, daemon=True)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send)
        send_thread.start()


client = ClientChat()
client.run()
