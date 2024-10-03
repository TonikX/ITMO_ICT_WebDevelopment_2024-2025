# Задание 3

## Описание

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: TCP

## Как запускать

1. Сервер:

   Листинг:
```python
import socket


headers = """HTTP/1.1 200 OK
            Content-Type: text/html\n\n"""
file = open(file='index.html').read()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(("127.0.0.1", 3000))

serv.listen(5)

while True:
    sock, _ = serv.accept()
    sock.recv(1024)
    sock.sendall(headers.encode())
    sock.sendall(file.encode())
```

   Запуск:
 ```bash
 python3 server.py
 ```

2. Клиент:

   Получить страницу возмонжо с помощью GET запроса localhost:3000, например, с помощью curl, Postman или открыть страницу в браузере. 