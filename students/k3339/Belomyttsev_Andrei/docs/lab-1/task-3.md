# Task 3

## Задание
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла `index.html`.

**Полезные ссылки:**

  - [ZetCode: Работа с сокетами](http://zetcode.com/python/socket/)

**Требования:**

  - Обязательно использовать библиотеку `socket`.

---

## HTTP server

You can choose specific IP address and port by changing `IP` and `PORT` variables.

In order to connect to the server enter `127.0.0.1:PORT` into your browser's URL field.

You'll see `index.html` web page.

---

## Code

3.py:
```python
import socket

IP = '127.0.0.1'
PORT = 2020

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
headers = b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
try:
  while True:
    client, address = server.accept()
    with open('index.html', 'rb') as f:
      content = f.read()
    client.send(headers + content)
    client.shutdown(socket.SHUT_WR)
except KeyboardInterrupt:
  server.close()
```