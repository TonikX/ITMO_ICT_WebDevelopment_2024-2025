import socket
import threading

HOST = 'localhost'
PORT = 9801


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = ((HOST, PORT))
        self.username = input("Enter your username: ")

    def connect(self):
        try:
            self.sock.connect(self.serverAddress)
            print("Connected to server")
            self.sock.send(self.username.encode('utf-8'))
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return

        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_messages(self):
        while True:
            message = input()
            if message == '/exit':
                self.sock.send(message.encode('utf-8'))
                print("You have left the chat")
                self.sock.close()
                break
            try:
                self.sock.send(message.encode('utf-8'))
            except:
                print("Error sending message, closing connection")
                self.sock.close()
                break

    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message:
                    print(message)
            except:
                print("Error receiving message, closing connection")
                self.sock.close()
                break


client = Client()
client.connect()