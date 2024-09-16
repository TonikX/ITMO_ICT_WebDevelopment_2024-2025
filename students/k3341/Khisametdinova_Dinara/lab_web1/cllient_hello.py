from client import Client

class EchoClient(Client):
    def send_and_receive(self):
        self.send_message("Hello, server")
        response = self.receive_response()
        print(f"Received from server: {response}")

if __name__ == "__main__":
    client = EchoClient(protocol_type="UDP")
    client.send_and_receive()
    client.close()
