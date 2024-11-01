import threading

from client import Client

class ChatClient(Client):
    def __init__(self, server_host='localhost', server_port=12345):
        super().__init__(protocol_type="TCP", server_host=server_host, server_port=server_port)

    def send_messages(self):
        while True:
            message = input()
            if message:
                self.send_message(message)

    def receive_messages(self):
        while True:
            try:
                message = self.receive_response()
                if message:
                    print(message)
            except:
                print("Connection to server lost.")
                break

    def start(self):
        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

if __name__ == "__main__":
    client = ChatClient()
    client.start()
