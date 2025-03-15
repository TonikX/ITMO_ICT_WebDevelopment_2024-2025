# Task 1

## Задание
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

**Требования:**

  - Обязательно использовать библиотеку `socket`.
  - Реализовать с помощью протокола UDP.

**Полезные ссылки:**

  - [Habr: Основы работы с сокетами](https://habr.com/ru/post/149077/)
  - [Андрей Малинин: Сокеты в Python](https://andreymal.org/socket3/)
  - [Документация Python: Руководство по сокетам](https://docs.python.org/3.6/howto/sockets.html)
  - [Python Library Reference: socket](https://docs.python.org/3.6/library/socket.html)
  - [Видео: Введение в работу с сокетами](https://www.youtube.com/watch?v=Lbfe3-v7yE0)

---

## UDP client and server

You can choose specific IP address and port by changing `IP` and `PORT` variables.

Firstly run `python 1-server.py`

Then run `python 1-client.py`

You'll see messages in both consoles: "*Hello, server*" and "*Hello, client*".

---

## Code

1-server.py:
```python
import socket

IP = '127.0.0.1'
PORT = 2020

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP, PORT))
data, address = server.recvfrom(1024)
print(data.decode('utf-8'))
server.sendto(b'Hello, client\n', address)
server.close()
```

1-client.py:
```python
import socket

IP = '127.0.0.1'
PORT = 2020

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'Hello, server\n', (IP, PORT))
data, address = client.recvfrom(1024)
print(data.decode('utf-8'))
client.close()
```