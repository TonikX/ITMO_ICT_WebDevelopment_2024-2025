# Task 4

Реализовать двухпользовательский или многопользовательский чат. Реализация
многопользовательского часа позволяет получить максимальное количество
баллов.
Реализовать с помощью протокола TCP – 100% баллов, с помощью UDP – 80%.

Обязательно использовать библиотеку threading.
Для реализации с помощью UDP, thearding использовать для получения
сообщений у клиента.

Для применения с TCP необходимо запускать клиентские подключения И прием
и отправку сообщений всем юзерам на сервере в потоках. Не забудьте сохранять юзеров,
чтобы потом отправлять им сообщения.

server_chat.py
```python
import threading

from server import Server

class ChatServer(Server):
    def __init__(self, host='localhost', port=12345):
        super().__init__(protocol_type="TCP", host=host, port=port)
        self.clients = {}  # {имя_пользователя: соединение}

    def broadcast(self, message, sender_name):
        for name, conn in self.clients.items():
            if name != sender_name:
                try:
                    conn.sendall(message.encode())
                except Exception as e:
                    print(f"Failed to send message to {name}: {e}")
                    self.clients.pop(name) 

    def private_message(self, message, recipient_name):
        if recipient_name in self.clients:
            try:
                self.clients[recipient_name].sendall(message.encode())
            except Exception as e:
                print(f"Failed to send private message to {recipient_name}: {e}")
                self.clients.pop(recipient_name)

    def handle_client(self, conn, addr):  #  в отдельном потоке
        print(f"New connection: {addr}")
        try:
            conn.send("Enter your name: ".encode())
            name = conn.recv(1024).decode()
            self.clients[name] = conn 

            conn.send(f"Welcome to the chat, {name}!".encode())
            print(f"{name} has joined the chat")

            while True:
                message = conn.recv(1024).decode()
                if not message:
                    break
                print(f"Received from {name}: {message}")

                if message.startswith('/pm'):   # '/pm' - лс
                    parts = message.split(' ', 2)
                    if len(parts) == 3:
                        recipient_name = parts[1]
                        private_message = f"Private from {name}: {parts[2]}"
                        self.private_message(private_message, recipient_name)
                    else:
                        conn.send("Usage: /pm recipient_name message".encode())
                else:
                    broadcast_message = f"{name}: {message}"
                    self.broadcast(broadcast_message, name)

        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            print(f"Client {name} disconnected")
            self.clients.pop(name, None)
            conn.close()

    def start(self):
        print(f"Server started at {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
```
client_chat.py
```python
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
```
