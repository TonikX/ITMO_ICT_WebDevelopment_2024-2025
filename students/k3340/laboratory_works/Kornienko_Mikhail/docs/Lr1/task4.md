# Задание 4

## Описание

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: TCP

## Как запускать

1. Сервер:

   Листинг:
```python
import socket
import threading


class ChatServer:
    def __init__(self, host="127.0.0.1", port=4000, max_connections=10):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(max_connections)
        self.users = {}

    def broadcast(self, sender_conn, message):
        for conn, name in self.users.items():
            if conn != sender_conn:
                try:
                    conn.send(f'{self.users[sender_conn]}: {message}'.encode())
                except Exception as e:
                    print(f"Error sending message to {name}: {e}")
                    conn.close()
                    self.remove_user(conn)

    def remove_user(self, conn):
        if conn in self.users:
            print(f"User {self.users[conn]} disconnected.")
            del self.users[conn]

    def handle_client(self, conn):
        try:
            while True:
                msg = conn.recv(1024).decode()
                if not msg or msg.lower() == 'quit':
                    self.remove_user(conn)
                    break
                self.broadcast(conn, msg)
        except ConnectionResetError:
            self.remove_user(conn)
        finally:
            conn.close()

    def start(self):
        print("Server started. Waiting for connections...")
        while True:
            conn, addr = self.server.accept()
            print(f"New connection from {addr}")
            name = conn.recv(1024).decode()
            self.users[conn] = name
            print(f"User {name} connected.")
            client_thread = threading.Thread(target=self.handle_client, args=(conn,))
            client_thread.start()


chat_server = ChatServer()
chat_server.start()
```

   Запуск:
```bash
python3 server.py
```
2. Клиент:

   Листинг:
```python
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
                message = input()
                self.connection.send(message.encode())
                time.sleep(2)
            except ConnectionError as e:
                print(f"Error sending message: {e}")
                break

    def start(self):
        if self.connect_to_server():
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.send_messages()


print("Type your name: ")
name = input()
client = ChatClient(name=name)
client.start()
```

   Для запуска клиентов:
 ```bash
 python3 client.py
 ```

   Затем вводите в консоль имя клиента и потом при каждый ввод в консоль является сообщением.