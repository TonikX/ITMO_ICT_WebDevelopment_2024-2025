# Задание:
Реализовать клиентскую и серверную часть приложения.
Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера.
В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## Требования:

- Обязательно использовать библиотеку socket.

- Реализовать с помощью протокола UDP.


# Клиент
```py
from socket import socket, AF_INET, SOCK_DGRAM


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.sendto(b"Hello, server", ("localhost", 8080))

    data, server = sock.recvfrom(1024)
    print(f"{data.decode()}")
```

# Сервер
```py
from socket import socket, AF_INET, SOCK_DGRAM


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.bind(("localhost", 8080))

    while True:
        data, addr = sock.recvfrom(1024)
        print(data.decode())

        sock.sendto(b"Hello, client", addr)
```
