# Task 1

Реализовать клиентскую и серверную часть приложения. Клиент отсылает серверу
сообщение «Hello, server». Сообщение должно отразиться на стороне сервера.
Сервер в ответ отсылает клиенту сообщение «Hello, client». Сообщение должно
отобразиться у клиента.
Обязательно использовать библиотеку socket
Реализовать с помощью протокола UDP

server_hello.py
```python
from server import Server

class EchoServer(Server):
    def handle_echo(self):
        data, client = self.handle_client() 
        print(f"Received: {data}")
        response = "Hello, UDP client"  
        self.send_response(response, client) 

if __name__ == "__main__":
    server = EchoServer(protocol_type="UDP")
    server.handle_echo()
    server.close()
```
client_hello.py
```python
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
```
