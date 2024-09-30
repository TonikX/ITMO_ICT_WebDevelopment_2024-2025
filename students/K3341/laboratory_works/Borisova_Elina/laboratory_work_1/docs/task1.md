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

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 8080))

while True:
    data, address = server.recvfrom(1024)
    server.sendto(b"Hello, client", address)
```
### client.py
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('localhost', 8080)

client.sendto(b"Hello, server", address)
data, server = client.recvfrom(1024)
print(data.decode('utf-8'))
client.close()
```