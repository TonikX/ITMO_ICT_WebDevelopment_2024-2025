# Лабораторная №1. Работа с сокетами

## Задание №1. Клиент-серверное общение через UDP
---
#### Условие
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

**Требования:**

* Обязательно использовать библиотеку `socket`.
* Реализовать с помощью протокола `UDP`.
    
#### Реализация
- Клиентская часть отправляет сообщение серверу и ожидает ответ.
- Сервер принимает сообщение от клиента, выводит его на экран и отправляет ответ.
- Используется библиотека `socket` для создания сокетов и обмена данными между клиентом и сервером по протоколу `UDP`.

#### Код
**`server.py`**
```
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostname(), 1234))

while True:
    try:
        data, addr = s.recvfrom(1024)
        udata = data.decode("utf-8")
        print(f"Connection established: {addr}")
        print("Received message: %s" % udata)
        MESSAGE = b'Hello, client!'
        s.sendto(MESSAGE, addr)
    except KeyboardInterrupt:
        s.close()
        break
```

**`client.py`**
```python
import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.connect((socket.gethostname(), 1234))
conn.send(b"Hello, server.\n")
msg = conn.recv(1024)
umsg = msg.decode('utf-8')
print(umsg)
```
<br>

## Задание №2. Клиент-серверное общение через TCP
---
#### Условие
Реализовать клиентскую и серверную части приложения. Клиент запрашивает выполнение математической операции (решение квадратного уравнения), параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Требования:**

* Использовать библиотеку `socket`.
* Реализовать с использованием протокола `TCP`.
    
#### Реализация
* Клиент запрашивает ввод коэффициентов квадратного уравнения и отправляет их на сервер.
* Сервер получает коэффициенты, решает уравнение и отправляет результат клиенту.
* Клиент получает результат и выводит его на экран.

#### Код
**`server.py`**
```python
import socket
import pickle
import math

def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant >= 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return root1, root2
    else:
        return "Корней нет"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(10)

while True:
    try:
        conn, addr = s.accept()
        data = conn.recv(1024)
        coefs = pickle.loads(data)

        a, b, c = coefs
        result = solve_quadratic(a, b, c)

        result_data = pickle.dumps(result)
        conn.send(result_data)

        conn.close()

    except KeyboardInterrupt:
        s.close()
        break
```

**`client.py`**
```python
import socket
import pickle

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((socket.gethostname(), 1234))

print("Введите коэффициенты квадратного уравнения: a, b, c\n")
a = int(input())
b = int(input())
c = int(input())
coefs = [a, b, c]

data = pickle.dumps(coefs)

conn.send(data)

result = conn.recv(1024)
result = pickle.loads(result)
print("Результат: ", result)

conn.close()
```

<br>

## Задание №3. HTTP-сервер для передачи HTML-страницы
---
#### Условие

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая загружается сервером из файла `index.html`.

**Требования:**

* Использовать библиотеку `socket`.
* Реализовать передачу HTML-страницы через `HTTP`.
  
#### Реализация

* Клиент отправляет HTTP-запрос серверу.
* Сервер читает HTML-страницу из файла `index.html` и формирует HTTP-ответ.
* HTML-страница отправляется клиенту, который может её отобразить в браузере.

#### Код

**`server.py`**

```python
import socket

def handle_request(client_socket):
    # Чтение запроса от клиента
    request = client_socket.recv(1024).decode()
    print(f"Получен запрос:\n{request}")

    # Формирование ответа
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += "Content-Length: {}\r\n".format(len(html_content))
    response += "\r\n"
    response += html_content

    client_socket.sendall(response.encode())

    client_socket.close()

with open("task3/index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))

server_socket.listen(5)
print("Сервер запущен на порту 8080")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")

        handle_request(client_socket)
finally:
    server_socket.close()
```

**`index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сервер</title>
</head>
<body>
    <h1>Привет, клиент!</h1>
</body>
</html>
```
<br>

## Задание №4. Многопользовательский чат, реализация потоков
---
#### Условие
Реализовать многопользовательский чат, в котором сервер принимает подключения нескольких клиентов и пересылает им сообщения. Все клиенты могут отправлять сообщения, которые будут отображаться у всех участников чата.

**Требования:**

* Использовать библиотеку `socket`.
* Для обработки каждого клиента использовать библиотеку `threading`.
* Реализовать с использованием протокола `TCP`.

#### Реализация

* Сервер запускает сокет, слушает подключения клиентов и обрабатывает их в отдельных потоках.
* Каждый клиент подключается к серверу, получает приветственное сообщение и может отправлять и получать сообщения в чате.
* Сообщения от клиента передаются серверу, который пересылает их всем остальным клиентам.

**Функции сервера:**

`remove_client(client_socket)` — удаляет клиента из списка подключенных клиентов, если соединение закрывается.  
`broadcast_message(message, sender_socket, sender_address)` — пересылает сообщение от одного клиента всем остальным подключенным клиентам. Если отправка сообщения не удалась, клиент удаляется из списка.  
`handle_client(client_socket, client_address)` — обрабатывает сообщения от конкретного клиента и пересылает их другим клиентам. Завершает работу, если соединение закрывается.  
`start_server()` — создает сокет, запускает сервер на заданном порту и обрабатывает подключения клиентов.  

**Функции клиента:**

`receive_messages(client_socket)` — получает и отображает сообщения от сервера.  
`send_messages(client_socket)` — отправляет введенные пользователем сообщения на сервер.  
`start_client()` — создает сокет, подключается к серверу, и запускает потоки для обработки сообщений.  

#### Код

**`server.py`**

```python
import socket
import threading

CLIENTS = []

def remove_client(client_socket):
    if client_socket in CLIENTS:
        CLIENTS.remove(client_socket)

def broadcast_message(message, sender_socket, sender_address):
    for client_socket in CLIENTS:
        if client_socket != sender_socket:
            try:
                msg = str(sender_address[1]) + ': ' + message
                client_socket.send(msg.encode('utf-8'))
            except:
                client_socket.close()
                remove_client(client_socket)

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(2056).decode('utf-8')
            if message:
                broadcast_message(message, client_socket, client_address)
            else:
                break
        except:
            break
    client_socket.close()
    remove_client(client_socket)

def start_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1234))
        s.listen(10)
        print("Сервер запущен и слушает порт 1234...")
        while True:
            client_socket, client_address = s.accept()
            client_socket.send(b'You connected successfully.')
            print(f"Подключен клиент: {client_address}")
            CLIENTS.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        s.close()

if __name__ == '__main__':
    start_server()
```

**`client.py`**

```python
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(2056).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break
    client_socket.close()

def send_messages(client_socket):
    while True:
        new_msg = input()
        client_socket.send(new_msg.encode('utf-8'))

def start_client():
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((socket.gethostname(), 1234))

        welcome_msg = conn.recv(1024).decode()
        print(welcome_msg)

        receive = threading.Thread(target=receive_messages, args=(conn,))
        receive.start()
        send = threading.Thread(target=send_messages, args=(conn,))
        send.start()

    except KeyboardInterrupt:
        conn.close()

if __name__ == '__main__':
    start_client()
```

<br>

## Задание №5. Веб-сервер для обработки GET и POST HTTP-запросов
---

#### Условие
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

**Требования:**  

* Сервер должен принять и записать информацию о дисциплине и оценке по дисциплине.
* Сервер должен отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

#### Реализация

- Веб-сервер написан с использованием базовых сокетов на Python.
- Обрабатываются GET и POST запросы.
    - <span style='color: #e83e8c'>**POST**</span> запрос добавляет новую дисциплину или оценку по дисциплине.
    - <span style='color: #e83e8c'>**GET**</span> запросы возвращают список дисциплин или информацию по оценкам.
- Данные дисциплин хранятся в памяти в формате словаря. Для каждой дисциплины хранится её ID, название и список оценок.
- Для каждого запроса сервер проверяет заголовки и параметры. В случае успешного запроса возвращается корректный ответ с данными.

**Детали реализации:**

1. **Основной серверный класс MyHTTPServer**  
Конструктор принимает параметры: хост, порт и имя сервера. Сервер хранит информацию о дисциплинах и их оценках в словаре.  
Основная функция `serve_forever()` открывает сокет, слушает подключения и передает клиентские запросы на обработку.  
2. **Обработка запросов**  
Метод `parse_request()` — принимает и разбирает запрос клиента: метод, путь и версию HTTP, заголовки и параметры.  
Метод `handle_request()` — выполняет основную логику обработки запросов:  
Для POST-запроса на /subjects сервер добавляет новую дисциплину.  
Для POST-запроса на /subjects/<id> добавляется оценка к существующей дисциплине.  
Для GET-запроса на /subjects возвращается список всех дисциплин.  
Для GET-запроса на /subjects/<id> возвращается список оценок по конкретной дисциплине.  
Метод `send_response()` — отправляет ответ клиенту, формируя заголовки и тело ответа.  
3. **Форматы ответов**   
GET-запросы могут возвращать данные как в формате `HTML`, так и в формате `JSON` в зависимости от содержимого заголовка Accept.  
POST-запросы не возвращают тело ответа, только статус успешного выполнения (204 No Content).  

**Примеры запросов:**

* Добавление дисциплины
```http
POST /subjects?name=ComputerScience HTTP/1.1
Host: example.local
```

* Добавление оценки  
```http
POST /subjects/1?mark=5 HTTP/1.1
Host: example.local
```

* Получение списка дисциплин
```http
GET /subjects HTTP/1.1
Host: example.local
Accept: text/html
```

* Получение оценок по дисциплине  
```http
GET /subjects/1 HTTP/1.1
Host: example.local
Accept: application/json
```

#### Код

**`server.py`**

```python
import socket
import sys
from email.parser import Parser

from exceptions import HTTPError
from utils import Request, Response
import json

MAX_LINE = 64 * 1024
MAX_HEADERS = 100

# py task5/server.py 127.0.0.1 53210 example.local
# python3 task5/server.py 127.0.0.1 53210 example.local

class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._subjects = {}

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print("Client serving failed", e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()

    def parse_request(self, conn):
        rfile = conn.makefile("rb")
        method, target, version = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)

        host = headers.get("Host")
        if not host:
            raise HTTPError(400, "Bad request", "Host header is missing")
        if host not in (self._server_name, f"{self._server_name}:{self._port}"):
            raise HTTPError(404, "Not found")

        print(method, target, version, headers)
        return Request(method, target, version, headers, rfile)

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(400, "Bad request", "Request line is too long")

            if line in (b"\r\n", b"\n", b""):
                # завершаем чтение заголовков
                break

            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise Exception("Too many headers")

        sheaders = b"".join(headers).decode("iso-8859-1")
        return Parser().parsestr(sheaders)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise Exception("Request line is too long")

        req_line = str(raw, "iso-8859-1")
        req_line = req_line.rstrip("\r\n")
        words = req_line.split()
        if len(words) != 3:
            raise Exception("Malformed request line")

        method, target, version = words
        if version != "HTTP/1.1":
            raise Exception("Unexpected HTTP version")

        return method, target, version

    def handle_request(self, req):
        if req.path == "/subjects" and req.method == "POST":
            return self.handle_post_subject(req)

        if req.path.startswith("/subjects/"):
            subj_id = req.path[len("/subjects/") :]
            if subj_id.isdigit():
                if req.method == "GET":
                    return self.handle_get_marks(req, subj_id)
                if req.method == "POST":
                    return self.handle_add_mark(req, subj_id)

        if req.path == "/subjects" and req.method == "GET":
            return self.handle_get_subjects(req)

        raise HTTPError(404, "Not found")

    def handle_post_subject(self, req):
        subj_id = len(self._subjects) + 1
        self._subjects[subj_id] = {
            "id": subj_id,
            "name": req.query["name"][0],
            "marks": [],
        }
        return Response(204, "Created")

    def handle_get_marks(self, req, subj_id):
        subj = self._subjects.get(int(subj_id))
        if not subj:
            raise HTTPError(404, "Not found")

        accept = req.headers.get("Accept")
        if "text/html" in accept:
            contentType = "text/html; charset=utf-8"
            body = "<html><head></head><body>"
            body += f"<div>Оценки по дисциплине {subj['name']}:</div>"
            body += "<ul>"
            for u in subj["marks"]:
                body += f"<li>{u}</li>"
            body += "</ul>"
            body += "</body></html>"

        elif "application/json" in accept:
            contentType = "application/json; charset=utf-8"
            body = json.dumps(subj)

        else:
            return Response(406, "Not Acceptable")

        body = body.encode("utf-8")
        headers = [("Content-Type", contentType), ("Content-Length", len(body))]
        return Response(200, "OK", headers, body)

    def handle_add_mark(self, req, subj_id):
        mark = req.query.get("mark")[0]
        self._subjects[int(subj_id)]["marks"].append(mark)
        return Response(204, "Subject marks updated")

    def handle_get_subjects(self, req):
        accept = req.headers.get("Accept")
        if "text/html" in accept:
            contentType = "text/html; charset=utf-8"
            body = "<html><head></head><body>"
            body += f"<div>Дисциплины ({len(self._subjects)})</div>"
            body += "<ul>"
            for u in self._subjects.values():
                body += f'<li>#{u["id"]} {u["name"]}</li>'
            body += "</ul>"
            body += "</body></html>"

        elif "application/json" in accept:
            contentType = "application/json; charset=utf-8"
            body = json.dumps(self._subjects)

        else:
            return Response(406, "Not Acceptable")

        body = body.encode("utf-8")
        headers = [("Content-Type", contentType), ("Content-Length", len(body))]
        return Response(200, "OK", headers, body)

    def send_response(self, conn, resp):
        wfile = conn.makefile("wb")
        status_line = f"HTTP/1.1 {resp.status} {resp.reason}\r\n"
        wfile.write(status_line.encode("iso-8859-1"))

        if resp.headers:
            for key, value in resp.headers:
                header_line = f"{key}: {value}\r\n"
                wfile.write(header_line.encode("iso-8859-1"))

        wfile.write(b"\r\n")

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode("utf-8")
        except:
            status = 500
            reason = b"Internal Server Error"
            body = b"Internal Server Error"
        resp = Response(status, reason, [("Content-Length", len(body))], body)
        self.send_response(conn, resp)


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]

    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
```

**`utils.py`**
```python
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
```

**`exceptions.py`**

```python
class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body
```