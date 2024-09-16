## Базовый класс сервера
Вынесу классы сервера и клиента в отдельные, чтобы потом их использовать в реализации заданий.

server.py
```python
import socket

class Server:
    def __init__(self, protocol_type="UDP", host='localhost', port=12345):
        self.host = host
        self.port = port
        self.protocol_type = protocol_type

        if self.protocol_type == "UDP":
            self.socket = self._create_UDP_socket()
        elif self.protocol_type == "TCP":
            self.socket = self._create_TCP_socket()
        else:
            raise ValueError("Invalid protocol type! Choose either 'UDP' or 'TCP'.")

    def _create_UDP_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        print(f"UDP Server started at {self.host}:{self.port}")
        return sock

    def _create_TCP_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print(f"TCP Server started at {self.host}:{self.port}, waiting for a connection...")
        return sock

    def handle_client(self):
        if self.protocol_type == "UDP":
            return self.handle_UDP_client()
        elif self.protocol_type == "TCP":
            return self.handle_TCP_client()

    def handle_UDP_client(self) -> tuple:
        print("Waiting for message from UDP client...")
        data, client_address = self.socket.recvfrom(1024)
        decoded_data = data.decode()
        print(f"Received from client: {decoded_data}")
        return decoded_data, client_address

    def handle_TCP_client(self) -> tuple:
        conn, client_address = self.socket.accept()
        print(f"Connected by: {client_address}")
        data = conn.recv(1024)
        decoded_data = data.decode()
        print(f"Received from client: {decoded_data}")
        return decoded_data, conn

    def send_response(self, response: str, client):
        if self.protocol_type == "UDP":
            data, client_address = client   # отправляю данные и адрес клиента
            self.socket.sendto(response.encode(), client_address)
            print(f"Sent to UDP client: {response}")
        elif self.protocol_type == "TCP":   # отправляю данные через соединение
            conn = client
            conn.sendall(response.encode())
            conn.close()
            print(f"Sent to TCP client: {response}")

    def close(self):
        self.socket.close()
        print("Server socket closed.")


```
## Базовый класс клиента
client.py
```python

import socket

class Client:
    def __init__(self, protocol_type="UDP", server_host='localhost', server_port=12345):
        self.server_host = server_host
        self.server_port = server_port
        self.protocol_type = protocol_type

        if self.protocol_type == "UDP":
            self.socket = self._create_UDP_socket()
        elif self.protocol_type == "TCP":
            self.socket = self._create_TCP_socket()
        else:
            raise ValueError("Invalid protocol type! Choose either 'UDP' or 'TCP'.")

    def _create_UDP_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sock

    def _create_TCP_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_host, self.server_port))
        return sock

    def send_message(self, message: str):
        print(f"Sending message to server: {message}")
        if self.protocol_type == "UDP":
            self.socket.sendto(message.encode(), (self.server_host, self.server_port))
        elif self.protocol_type == "TCP":
            self.socket.send(message.encode())

    def receive_response(self) -> str:
        if self.protocol_type == "UDP":
            data, _ = self.socket.recvfrom(1024)
        elif self.protocol_type == "TCP":
            data = self.socket.recv(1024)

        decoded_data = data.decode()
        return decoded_data

    def close(self):
        self.socket.close()
        print("Client socket closed.")

```