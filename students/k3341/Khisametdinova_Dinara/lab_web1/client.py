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
