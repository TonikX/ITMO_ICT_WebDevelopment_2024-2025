# Лабораторная работа #1
## Выполнил: Залетов Артём Дмитриевич, группа К3339
## Задание #1

**Задание:** Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  

**Клиент:**
```
import socket
def udp_client(host='127.0.0.1', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = 'Hello, server'
    sock.sendto(message.encode(), (host, port))
    data, addr = sock.recvfrom(1024)  # Буфер 1024 байта
    print(f"Получено сообщение : {data.decode()}")

if __name__ == "__main__":
    udp_client()
```

**Сервер:**
```
import socket
def udp_server(host='127.0.0.1', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Сервер запущен")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Получено сообщение: {data.decode()}")
        response = 'Hello, client'
        sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    udp_server()
```
## Задание #2

**Задание:** Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту. 

**Клиент:**
```
import socket
def get_positive_number(numb):
    while True:
        try:
            value = float(input(numb))
            if value > 0:
                return value
            else:
                print("Ошибка: значение должно быть положительным.")
        except ValueError:
            print("Ошибка: введено неверное число.")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    a = get_positive_number("Введите длину первого катета: ")
    b = get_positive_number("Введите длину второго катета: ")
    data = f"{a},{b}"
    client_socket.sendall(data.encode())
    result = client_socket.recv(1024).decode()
    print(f"Гипотенуза: {result}")
    client_socket.close()

if __name__ == '__main__':
    start_client()
```

**Сервер:**
```
import socket
import math
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            a, b = map(float, data.split(','))
            c = math.sqrt(a ** 2 + b ** 2)
            conn.sendall(str(c).encode())
        except Exception as e:
            conn.sendall(f"Ошибка: {str(e)}".encode())
        finally:
            conn.close()
if __name__ == '__main__':
    start_server()
```
## Задание #3

**Задание:** Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

**Клиент:**
```
import socket
def main():
    host = '127.0.0.1'
    port = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)
        client_socket.sendall(request.encode())
        response = client_socket.recv(4096).decode()
        print("Ответ сервера:\n", response)
if __name__ == "__main__":
    main()
```

**Сервер:**
```
import socket
def start_server(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        while True:
            client_socket, _ = server_socket.accept()
            with client_socket:
                request = client_socket.recv(1024).decode()
                print(request)
                if 'GET / HTTP/1.1' in request:
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                    try:
                        with open('index.html', 'r', encoding='utf-8') as f:
                            content = f.read()
                            response += content
                    except FileNotFoundError:
                        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
                client_socket.sendall(response.encode())
if __name__ == "__main__":
    start_server()
```

## Задание #4

**Задание:** Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

**Клиент:**
```
import socket
import threading

class Client:
    def __init__(self, ip, port, encoding="utf-8", buffer_size=1024):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        print("Connected to the server")

        self.encoding = encoding
        self.buffer_size = buffer_size

        self.receive_thread = threading.Thread(target=self.receive_thread_method)
        self.receive_thread.start()

        self.send_thread = threading.Thread(target=self.send_thread_method)
        self.send_thread.start()

    def disconnect(self):
        self.running = False
        self.sock.close()
        print("Disconnected from the server")

    def send_message(self, message: str):
        self.sock.sendall(message.encode(self.encoding))

    def receive_thread_method(self):
        print("Started receiving the messages from the server")
        while self.running:
            try:
                message = self.sock.recv(self.buffer_size).decode(self.encoding)
                print(message)
            except:
                self.disconnect()
                break

    def send_thread_method(self):
        while self.running:
            self.send_message(input())

if __name__ == "__main__":
    server_addr = "localhost"
    server_port = 8080
    Client(server_addr, server_port)

```

**Сервер:**
```
import socket
import threading
from dataclasses import dataclass
from enum import Enum

class UserState(Enum):
    NONE = -1
    CONNECTED = 0
    READY = 1

@dataclass
class User:
    conn: socket.socket
    state: UserState = UserState.NONE
    name: str = ""

class Server:
    def __init__(self, ip, port):
        self.running = True
        self.users: list[User] = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen()
        print("Server is listening")

        self.receive()

    def stop(self):
        self.running = False
        self.sock.close()
        print("Server stopped")

    def broadcast(self, label: str, message: str, except_list: list[User] = None):
        if except_list is None:
            except_list = []

        full_message = f"{label}: {message}"
        print(full_message)

        for user in self.users:
            if user.state != UserState.READY or user in except_list:
                continue
            user.conn.sendall(full_message.encode(encoding))

    def send_message(self, user: User, message: str):
        user.conn.sendall(message.encode(encoding))

    def process_user(self, conn: socket.socket):
        user = User(conn=conn, state=UserState.CONNECTED, name="")
        self.users.append(user)
        while self.running:
            try:
                if user.state == UserState.NONE:
                    user.state = UserState.CONNECTED
                elif user.state == UserState.CONNECTED:
                    self.send_message(user, "What is your name?")
                    name = conn.recv(buffer_size).decode(encoding)
                    if not name:
                        raise ValueError()

                    user.name = name
                    user.state = UserState.READY
                    self.broadcast(user.name, "connected")
                elif user.state == UserState.READY:
                    message = conn.recv(buffer_size).decode(encoding)
                    self.broadcast(user.name, message, [user])
            except:
                conn.close()
                self.users.remove(user)
                self.broadcast(user.name, "disconnected")
                break

    def receive(self):
        while self.running:
            conn, addr = self.sock.accept()
            print("Incoming connection", addr)

            thread = threading.Thread(target=self.process_user, args=(conn,))
            thread.start()

if __name__ == "__main__":
    encoding = "utf-8"
    buffer_size = 1024
    server_addr = "localhost"
    server_port = 8080
    Server(server_addr, server_port)

```

## Задание #5

**Задание:** Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.
**Сервер должен:**
* Принять и записать информацию о дисциплине и оценке по дисциплине.
* Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.


**Сервер:**
```
import socket
from urllib.parse import parse_qs

grades = {}


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self.host, self.port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Fail', e)
        finally:
            serv_sock.close()

    def serve_client(self, client):
        try:
            req = self.parse_request(client)
            resp = self.handle_request(req)
            self.send_response(client, resp)
        except ConnectionResetError:
            client = None

        if client:
            client.close()

    def parse_request_line(self, rfile):
        line = rfile.readline()
        line = line.decode('utf-8')
        return line.split()

    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)

        request = {'data': {}, 'method': method}

        if method == 'POST':
            content_length = 0
            headers = []
            while True:
                header_line = rfile.readline().decode('utf-8')
                if header_line == '\r\n':
                    break
                headers.append(header_line.strip())

                if header_line.lower().startswith('content-length'):
                    content_length = int(header_line.split(':')[1].strip())

            body = rfile.read(content_length).decode('utf-8')
            request['data'] = parse_qs(body)

        elif '?' in target:
            request['method'] = 'GET'
            values = target.split('?')[1].split('&')
            for value in values:
                a, b = value.split('=')
                request['data'][a] = b

        return request

    def handle_request(self, req):
        if req['method'] == 'POST':
            return self.handle_post(req)
        else:
            return self.handle_get()

    def handle_get(self):
        content_type = 'text/html; charset=utf-8'
        body = '''
        <html>
        <head>
            <style>
                body {
                    background-color: #f4f7f6;
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }

                .container {
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 80%;
                    max-width: 600px;
                }

                h1 {
                    text-align: center;
                    color: #fa8e47;
                    font-size: 36px;
                    margin-bottom: 20px;
                }

                .form-group {
                    margin-bottom: 20px;
                }

                .form-group label {
                    font-size: 18px;
                    color: #555;
                    display: block;
                    margin-bottom: 5px;
                }

                .form-group input {
                    width: 100%;
                    padding: 12px;
                    font-size: 16px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    transition: border-color 0.3s;
                }

                .form-group input:focus {
                    border-color: #fa8e47;
                    outline: none;
                }

                .form-group button {
                    width: 100%;
                    padding: 14px;
                    background-color: #fa8e47;
                    color: #fff;
                    font-size: 18px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }

                .form-group button:hover {
                    background-color: #e07c3c;
                }

                table {
                    width: 100%;
                    margin-top: 30px;
                    border-collapse: collapse;
                }

                table th, table td {
                    padding: 12px;
                    text-align: center;
                    border: 1px solid #ddd;
                    font-size: 18px;
                }

                table th {
                    background-color: #fa8e47;
                    color: #fff;
                }

                table tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Добавить оценку</h1>
                <form method="post">
                    <div class="form-group">
                        <label for="discipline">Предмет</label>
                        <input type="text" id="discipline" name="discipline" required />
                    </div>
                    <div class="form-group">
                        <label for="grade">Оценка</label>
                        <input type="number" id="grade" name="grade" min="1" max="5" required />
                    </div>
                    <div class="form-group">
                        <button type="submit">Добавить</button>
                    </div>
                </form>

                <table>
                    <thead>
                        <tr>
                            <th>Дисциплина</th>
                            <th>Оценки</th>
                        </tr>
                    </thead>
                    <tbody>
        '''
        for subject in grades:
            body += f'<tr> <td>{subject}</td> <td>{", ".join(grades[subject])}</td> </tr>'
        body += '''
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        '''
        body = body.encode('utf-8')
        headers = [('Content-Type', content_type)]
        return Response(200, 'OK', headers, body)

    def handle_post(self, request):
        discipline = request['data']['discipline'][0]
        grade = request['data']['grade'][0]

        if discipline not in grades:
            grades[discipline] = []
        if 1 <= int(grade) <= 5:
            grades[discipline].append(grade)

        return self.handle_get()

    def send_response(self, conn, resp):
        rfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        rfile.write(status_line.encode('utf-8'))

        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                rfile.write(header_line.encode('utf-8'))

        rfile.write(b'\r\n')

        if resp.body:
            rfile.write(resp.body)

        rfile.flush()
        rfile.close()


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


if __name__ == '__main__':
    serv = MyHTTPServer('127.0.0.1', 8080)
    serv.serve_forever()

```


