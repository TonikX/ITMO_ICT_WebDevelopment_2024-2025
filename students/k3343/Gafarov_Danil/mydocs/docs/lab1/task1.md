# Задание 1
Реализовать клиентскую и серверную часть приложения с помощью протокола UDP.
## Сервер
Листинг кода серверной части:
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Socket created')

# Привязываем сокет к адресу и порту
HOST = 'localhost'
PORT = 8080
s.bind((HOST, PORT))
print('Socket bind complete')

while True:
    message, address = s.recvfrom(1024)
    print(f"New message from client: {message.decode()}")

    response = 'Hello, UDP Client!'
    s.sendto(response.encode(), address)
    print(f"Message sent to client: {response}")
```
## Клиент
Листинг кода клиентской части:
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = 'localhost'
PORT = 8080
address = HOST, PORT
message = "Hi, UDP server!"

s.sendto(message.encode(), address)
print(f"Sent message to server: {message}")

response, server_address = s.recvfrom(1024)
print(f"Got reply from server: {response.decode()}")
s.close()
```
## Объяснение
Запускаем файл сервера, затем клиента; сервер ожидает сообщение от клиента и посылает ответ. Обмен происходит при помощи протокола UDP(параметр socket.SOCK_DGRAM)