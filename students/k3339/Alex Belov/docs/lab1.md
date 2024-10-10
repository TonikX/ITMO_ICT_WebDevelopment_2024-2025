#Лабораторная работа №1

##Задание №1

В одном файле реализован функционал клиента и сервера с возможностью выбора режима запуска.
Сервер в бесконечном цикле слушает сообщения от клиента, отвечая при получении сообщения "Hello, server!" текстом "Hello, client!"
```
import socket


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54001)
    server_socket.bind(server_address)
    print("Сервер запущен и ожидает сообщений...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Сообщение от клиента: {message.decode('utf-8')}")

        reply = "Hello, client"
        server_socket.sendto(reply.encode('utf-8'), client_address)


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54001)

    message = "Hello, server"
    client_socket.sendto(message.encode('utf-8'), server_address)

    reply, _ = client_socket.recvfrom(1024)
    print(f"Ответ от сервера: {reply.decode('utf-8')}")

    client_socket.close()


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()
    else:
        print("Некорректный выбор. Пожалуйста, выберите 'server' или 'client'.")
```

## Задание №2

Реализован клиент-серверный вариант решения простейшей задачи нахождения длины гипотенузы по двум катетам.
```
import socket
import math


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54002)
    server_socket.bind(server_address)
    print("Сервер запущен и ожидает запросов...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        a, b = map(float, message.decode('utf-8').split(','))
        print(f"Получены катеты: a={a}, b={b}")

        c = math.sqrt(a ** 2 + b ** 2)
        print(f"Вычисленная гипотенуза: c={c}")

        server_socket.sendto(str(c).encode('utf-8'), client_address)


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54002)

    a = float(input("Введите длину первого катета: "))
    b = float(input("Введите длину второго катета: "))

    message = f"{a},{b}"
    client_socket.sendto(message.encode('utf-8'), server_address)

    reply, _ = client_socket.recvfrom(1024)
    print(f"Результат (гипотенуза): {reply.decode('utf-8')}")

    client_socket.close()


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()
    else:
        print("Некорректный выбор. Пожалуйста, выберите 'server' или 'client'.")
```

## Задание №3

Реализован функционал получения страницы `index.html` с использованием библиотеки `socket`

```
import socket
import math


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)
    print("Сервер запущен и ожидает запросов...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        if message.decode('utf-8') == "gimme index.html":
            with open("index.html") as f:
                server_socket.sendto(str(f.read()).encode('utf-8'), client_address)


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 8080)

    client_socket.sendto("gimme index.html".encode('utf-8'), server_address)

    reply, _ = client_socket.recvfrom(1024)
    print(reply.decode('utf-8'))

    client_socket.close()


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()
    else:
        print("Некорректный выбор. Пожалуйста, выберите 'server' или 'client'.")
```

## Задание №4

Реализован мультипользовательский чат

```
import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
clients = []


def handle_client(client_socket, client_address):
    print(f"New connection: {client_address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"{client_address} said: {message}")

            broadcast_message(message, client_socket)
    except ConnectionResetError:
        print(f"{client_address} disconnected")
    finally:
        clients.remove(client_socket)
        client_socket.close()


def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started at {SERVER_HOST}:{SERVER_PORT}, waiting for clients...")

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input("You: ")
            client_socket.send(message.encode('utf-8'))
    finally:
        client_socket.close()


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\nNew message: {message}")
        except:
            print("Connection closed...")
            break


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()
```

## Задание №5

Реализован веб-сервер с использованием базового класса, позволяющий сохранять и получать оценки по нескольким дисциплинам.

```
import socket
from urllib.parse import urlparse, parse_qs


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.grades = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Сервер запущен на {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f"Подключение от {addr}")
                    self.serve_client(client_socket)

    def serve_client(self, client_socket):
        request_data = client_socket.recv(1024).decode('utf-8')
        if not request_data:
            return

        method, url, headers, body = self.parse_request(request_data)
        print(f"Метод: {method}, URL: {url}")

        if method == "GET":
            self.handle_get(client_socket)
        elif method == "POST":
            self.handle_post(client_socket, body)

    def parse_request(self, request_data):
        request_lines = request_data.split("\r\n")
        method, url, protocol = request_lines[0].split(" ")
        headers = {}
        body = ""

        i = 1
        while request_lines[i]:
            header_name, header_value = request_lines[i].split(": ", 1)
            headers[header_name] = header_value
            i += 1

        if "Content-Length" in headers:
            content_length = int(headers["Content-Length"])
            body = request_lines[-1][:content_length]

        return method, url, headers, body

    def handle_get(self, client_socket):
        response_body = open("index.html", encoding="utf-8").read()

        grades = ("<table class='table'>"
                  "<thead>"
                      "<tr>"
                          "<th scope='col'>Дисциплина</th>"
                          "<th scope='col'>Оценки</th>"
                      "</tr>"
                  "</thead><tbody>")
        for subject, grade in self.grades.items():
            grades += f"<tr><td>{subject}</td><td>"
            for _grade in grade:
                grades += f"<span class='m-1 badge text-bg-success'>{_grade}</span>"
            grades += "</td></tr>"
        if len(self.grades) == 0:
            grades += f"<tr><td>Данных пока нет :(</td><td></td></tr>"
        grades += "</tbody></table>"

        response_body = response_body.replace("%GRADES%", grades)

        self.send_response(client_socket, "200 OK", response_body)

    def handle_post(self, client_socket, body):
        params = parse_qs(body)
        subject = params.get('subject', [''])[0]
        grade = params.get('grade', [''])[0]

        if subject and grade:
            if subject in self.grades.keys():
                self.grades[subject].append(grade)
            else:
                self.grades[subject] = [grade]
            self.handle_get(client_socket)
        else:
            self.send_response(client_socket, "400 Bad Request", "Ошибка: отсутствуют необходимые параметры")

    def send_response(self, client_socket, status, body):
        response = f"HTTP/1.1 {status}\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        client_socket.sendall(response.encode('utf-8'))


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    server = MyHTTPServer(host, port)
    server.serve_forever()
```