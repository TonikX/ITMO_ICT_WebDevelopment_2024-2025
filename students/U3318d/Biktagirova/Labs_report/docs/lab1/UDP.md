#

## Задание 1:
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Требования:

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола UDP.

`Server's code`

``` py
import socket

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = 'localhost'
PORT = 8888
SERVER_MESSAGE = "Hello, client"
BUFF_SIZE = 1024
SERVER_MESSAGE_IN_BYTES = SERVER_MESSAGE.encode()

serv_socket.bind((HOST, PORT))
print("UDP server is running on", HOST, ':', PORT)

while True:
    try:
        # получаем данные размера BUFF_SIZE
        CLIENT_MESSAGE, address = serv_socket.recvfrom(BUFF_SIZE)
        # отправляем сообщение клиенту
        serv_socket.sendto(SERVER_MESSAGE_IN_BYTES, address)

        # выводим полученное сообщение от клиента декодированное из байтовой строки в строку
        print(CLIENT_MESSAGE.decode())

    except KeyboardInterrupt:
        print(f"Closing server on {HOST}:{PORT}")
        serv_socket.close()
        break

```

`Client's code`

``` py
import socket

# UDP
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = 'localhost'
PORT = 8888
CLIENT_MESSAGE = "Hello, server"
CLIENT_MESSAGE_IN_BYTES = CLIENT_MESSAGE.encode()
BUFF_SIZE = 1024

# подключаемся
client_sock.connect((HOST, PORT))

# отправляем сообщение
client_sock.send(CLIENT_MESSAGE_IN_BYTES)

# а это можно использовать без отдельного connect
# client_sock.sendto(CLIENT_MESSAGE_IN_BYTES, (HOST, PORT))

try:
    SERVER_MESSAGE = client_sock.recv(BUFF_SIZE).decode()
except ConnectionRefusedError:
    SERVER_MESSAGE = f'Sorry, connection to {HOST}:{PORT} is refused'

print(SERVER_MESSAGE)
```
