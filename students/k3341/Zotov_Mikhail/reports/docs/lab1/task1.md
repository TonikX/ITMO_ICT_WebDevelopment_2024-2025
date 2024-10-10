# Задание 1<br><br>

### Условие
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

#### Требования:
- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола UDP.
---

### Код

#### Сервер
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создаем сокет (AF_INET - IPv4, SOCK_DGRAM - UDP)
sock.bind(('localhost', 2024))  # Определяем ip хоста и номер порта
print("Server listening on port 2024")
message = "Hello, client"

while True:
    data, client_addr = sock.recvfrom(1024)
    print(data.decode())
    sock.sendto(message.encode(), client_addr)
```
#### Клиент
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Hello, server"

sock.sendto(message.encode(), ('localhost', 2024))
data, server = sock.recvfrom(1024)
print(data.decode())

sock.close()
```