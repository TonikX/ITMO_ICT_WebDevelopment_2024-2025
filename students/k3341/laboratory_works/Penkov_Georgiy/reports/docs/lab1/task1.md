# Лабораторная 1, Задание 1
## Условие
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.
### Требования:
- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола UDP.
## Решение
`server.py`
```
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_ADDRESS = ("127.0.0.1", 1024)
MESSAGE = b"Hello, client!"
BUFFER_SIZE = 1024

print(f"Starting up on {SERVER_ADDRESS}")
server_socket.bind(SERVER_ADDRESS)

while True:
    print("Waiting to receive message..")
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Received message: {data}, from {client_address}")
    server_socket.sendto(MESSAGE, client_address)
    print(f"Sent message {MESSAGE} back to {client_address}")

```

`client.py`:
```
import socket

SERVER_ADDRESS = ("127.0.0.1", 1024)
MESSAGE = b"Hello, server!"
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    print(f"Sending {MESSAGE}")
    client_socket.sendto(MESSAGE, SERVER_ADDRESS)
    print("Waiting to receive..")
    response, server = client_socket.recvfrom(BUFFER_SIZE)
    print(f"Received {response} from {server}")
finally:
    client_socket.close()
    print("Socket closed")

```
