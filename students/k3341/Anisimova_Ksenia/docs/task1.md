# Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

---
### Требования:
- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола UDP.

---
### server.py

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Server is waiting for a client...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f"Message from client: {data.decode('utf-8')}")
    response_message = "Hello, client"
    server_socket.sendto(response_message.encode('utf-8'), client_address)
```
### client.py
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), server_address)
response, _ = client_socket.recvfrom(1024)

print(f"Message from server: {response.decode('utf-8')}")

client_socket.close()
```