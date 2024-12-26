# Задание 1

## Описание

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», которое должно отображаться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое отображается у клиента.

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: UDP

## Как запускать

1. Сервер:

   Листинг:

```python
import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.bind(("127.0.0.1", 1000))

while True:
    data, addr = serv.recvfrom(1024)
    print("Message:", data.decode())
    serv.sendto("Hello, client".encode(), addr)
```

   Запуск:
```bash
python3 server.py
```   

2. Клиент:

   Листинг:

```python
import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.sendto("Hello, server".encode(), ("127.0.0.1", 1000))

data, addr = serv.recvfrom(1024)
print("Message:", data.decode())
```

   Запуск:
 ```bash
 python3 client.py
 ```
