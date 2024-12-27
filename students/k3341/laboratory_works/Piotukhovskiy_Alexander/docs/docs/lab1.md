# Лабораторная работа 1. Работа с сокетами.

---

## Задание 1
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

**Требования:**
- Реализовать с помощью протокола UDP

**Реализация**  
Так как у нас протокол **UPD**, устанавливать предварительное соединение не нужно.  

**Клиент:**
```python
import socket

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode(), (HOST, PORT))

response, server_address = client.recvfrom(BUFFER_SIZE)
decoded_data = response.decode()
print(decoded_data)

client.close()
```

HOST - адрес сервера  
PORT - порт, который слушает сервер  
BUFFER_SIZE - максимальное количество байт, которое мы читаем за раз  

Так как протокол **UDP** не предоставляет гарантии доставки, предварительное соединение с сервером устанавливать не нужно. Мы просто создаем объект сокета (client), передавая ему в качестве аргументов **AF_INET** (означает, что мы используем в качестве сетевого протокола IPv4) и **SOCK_DGRAM** (означает, что мы используем в качестве транспортного протокола UDP). После этого мы отправляем серверу датаграмму с закодированным в **UTF-8** сообщением. Сервер отправляет ответное сообщение, которое мы читаем из нашего клиентского сокета с помощью метода **.recvfrom**, декодируем его и выводим на экран. В конце мы удаляем клиентский сокет с помощью метода **.close**.

**Сервер:**
```python
import socket

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print("Server is running")

while True:
    data, client_address = server.recvfrom(BUFFER_SIZE)
    decoded_data = data.decode()
    print(decoded_data)
    server.sendto("Hello, client".encode(), client_address)
    if decoded_data == "stop_server":
        break
server.close()
```

HOST - адрес для прослушивания  
PORT - порт для прослушивания  
BUFFER_SIZE - максимальное количество байт, которое мы читаем за раз  

---

## Задание 2
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Требования:**
- Реализовать с помощью протокола TCP
- Задача по варианту: Поиск площади трапеции

**Реализация**  
В данном задании мы используем **TCP**, а не UDP. Этот протокол предоставляет гарантии доставки сообщений. Перед отправкой сообщения, необходимо установить соединение с сервером с помощью метода `.connect()`.

**Клиент:**
```python
import json
import socket

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024


a, b, h = map(
    lambda x: float(x.strip()),
    input("Введите длины двух оснований трапеции и высоту. \nРазделяйте значения запятой.\n").strip().split(","),
)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(json.dumps(dict(a=a, b=b, h=h)).encode())

response = client.recv(BUFFER_SIZE)
area = float(response.decode())

print(f"Площадь = {area}")
client.close()
```

**Сервер:**
```python
import json
import socket

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024
MAX_CONNECTIONS = 10


def calculate_area_trapezoid(a, b, h):
    return (a + b) * h / 2


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_CONNECTIONS)
print("Server is running")

while True:
    client, _ = server.accept()
    data = client.recv(BUFFER_SIZE)
    if data == "stop_server":
        break
    j = json.loads(data)
    a, b, h = j["a"], j["b"], j["h"]
    area_trapezoid = calculate_area_trapezoid(a, b, h)
    client.send(f"{area_trapezoid}".encode())
server.close()
```

---

## Задание 3
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла `index.html`.

**Реализация**  
Необходимо реализовать протокол **HTTP**, который работает поверх транспортного протокола **TCP**. Для этого мы добавляем спец данные (заголовки). Нам нужно отправить строки `HTTP/1.1 200 OK` и `Content-Type: text/html`.

**Сервер:**
```python
import os
import socket

HOST = "localhost"
PORT = 8080
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


def load_html_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        return None


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_CONNECTIONS)
print("Server is running")

while True:
    client, _ = server.accept()
    client.recv(BUFFER_SIZE)

    html = load_html_file("index.html")
    if html is not None:
        response = (
            (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(html)}\r\n"
                    "\r\n"
                    + html
            )
        )
    else:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<h1>404 Not Found</h1>"
        )
    client.sendall(response.encode())
```

---

## Задание 4
Реализовать многопользовательский чат.
**Требования:**
- Необходимо использовать библиотеку threading
- Протокол TCP
- Клиентские подключения и обработку сообщений от всех пользователей в потоках.

**Реализация**  
В данном задании был написан клиент, который умеет как отправлять, так и получать сообщения. Клиент должен выбрать никнейм и чат_айди перед тем, как ему будет позволено общаться с другими и читать их сообщения.

**Клиент:**
```python
import socket
import threading

HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 4

def receive_messages(client_socket):
    while True:
        try:
            message_length_data = client_socket.recv(BUFFER_SIZE)
            if not message_length_data:
                continue
            message_length = int.from_bytes(message_length_data, byteorder="big")
            message = client_socket.recv(message_length).decode('utf-8')
            if message:
                print(f"\n{message}")
        except:
            print("[-] Ошибка соединения с сервером.")
            client_socket.close()
            break


username = input("Введите свой никнейм: ")
chat_id = input("Введите id чата: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()


def send_message(client_socket, msg):
    msg = msg.encode()
    msg_length = len(msg).to_bytes(BUFFER_SIZE, byteorder='big')
    client_socket.sendall(msg_length + msg)


send_message(client_socket, f"/setup_nickname {username}")
send_message(client_socket, f"/join_chat {chat_id}")

while True:
    try:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        send_message(client_socket, message)
    except KeyboardInterrupt:
        client_socket.close()
        break
```

Сервер умеет обрабатывать сообщения в многопользовательских чатах с функциями установки никнеймов и присоединения к определённым чатам по идентификаторам. 
Клиенты могут отправлять команды для установки никнейма (`/setup_nickname`) и подключения к чату (`/join_chat`), а сервер транслирует их сообщения другим участникам того же чата. 
Для обработки каждого клиента создается отдельный поток, что позволяет обработке соединений работать параллельно. 
Сообщения передаются по протоколу **TCP**, а для их разделения используется механизм указания длины сообщения в заголовке каждого отправляемого пакета.


**Сервер:**
```python
import socket
import threading
import typing as tp
from dataclasses import dataclass

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 4

members = []


@dataclass
class ChatMember:
    client_socket: socket
    chat_id: str = None
    username: str = None


def handle_client(client_socket, client_address):
    print(f"[+] Новое подключение от {client_address}")
    members.append(ChatMember(client_socket=client_socket))

    while True:
        try:
            message_length_data = client_socket.recv(BUFFER_SIZE)
            if not message_length_data:
                continue
            message_length = int.from_bytes(message_length_data, byteorder="big")
            message = client_socket.recv(message_length).decode('utf-8')
            if message:
                member = find_chat_member(client_socket)
                print(f"[{client_address} :: {member.username}] {message}")

                if message[:16] == "/setup_nickname ":
                    if message[16:] == "":
                        send_message(client_socket, "[SYSTEM] Ошибка: вы не можете установить пустой никнейм.")
                        continue
                    if message[-6:].lower() == "system" or message[-5:].lower() == "(you)" or message[-4:].lower() in ["none", "null"]:
                        send_message(client_socket, "[SYSTEM] Ошибка: вы не можете установить этот никнейм.")
                        continue
                    old_username = member.username
                    member.username = message[16:]
                    if member.username == old_username:
                        send_message(client_socket, "[SYSTEM] У вас уже установлен этот никнейм.")
                        continue
                    if member.chat_id is not None:
                        broadcast_message(f"{old_username} сменил никнейм на {member.username}", member.chat_id, None, system_msg=True)
                    continue
                elif message[:11] == "/join_chat ":
                    if member.username is None:
                        send_message(client_socket, "[SYSTEM] Чтобы присоединиться к чату, вам нужно установить никнейм. Введите /setup_nickname <ваш никнейм>")
                        continue
                    if message[11:] == "":
                        send_message(client_socket, "[SYSTEM] Ошибка: вы не можете установить пустой айди чата.")
                        continue
                    old_chat_id = member.chat_id
                    member.chat_id = message[11:]
                    if member.chat_id == old_chat_id:
                        send_message(client_socket, "[SYSTEM] Вы уже в этом чате.")
                        continue
                    if old_chat_id is not None:
                        broadcast_message(f"{member.username} покинул чат.", old_chat_id, member.client_socket, system_msg=True)
                    broadcast_message(f"{member.username} зашёл в чат.", member.chat_id, None, system_msg=True)
                    continue
                if member.username is None:
                    send_message(client_socket, "[SYSTEM] Чтобы присоединиться к чату, вам нужно установить никнейм. Введите /setup_nickname <ваш никнейм>")
                elif member.chat_id is None:
                    send_message(client_socket, "[SYSTEM] Вы не присоединились к чату. Введите /join_chat <чат_айди>")
                else:
                    broadcast_message(message, member.chat_id, client_socket)
            else:
                break
        except ConnectionResetError:
            break

    print(f"[-] Отключен {client_address}")
    member = find_chat_member(client_socket)
    if member.chat_id is not None:
        target_chat_id = member.chat_id
        members.remove(member)
        broadcast_message(f"{member.username} покинул чат.", target_chat_id, client_socket, system_msg=True)
    remove_chat_member(client_socket)
    client_socket.close()


def find_chat_member(target_socket) -> tp.Union[ChatMember, None]:
    for member in members:
        if member.client_socket == target_socket:
            return member
    return None

def remove_chat_member(target_socket):
    for member in members:
        if member.client_socket == target_socket:
            members.remove(member)
            break


def broadcast_message(message, chat_id, sender_socket, system_msg: bool = False):
    sender = find_chat_member(sender_socket)
    for member in members:
        if member.chat_id == chat_id:
            try:
                full_message = ("[SYSTEM]" if system_msg else f"[{sender.username}{' (You)' if member.client_socket == sender_socket else ''}]") + f" {message}"
                send_message(member.client_socket, full_message)
            except:
                member.client_socket.close()
                members.remove(member)
                broadcast_message(f"{member.username} покинул чат.", chat_id, client_socket, system_msg=True)


def send_message(client_socket, message):
    msg = message.encode('utf-8')
    msg_length = len(msg).to_bytes(BUFFER_SIZE, byteorder='big')
    client_socket.sendall(msg_length + msg)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[*] Сервер запущен на {HOST}:{PORT}")

while True:
    client_socket, client_address = server.accept()

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
```

---

## Задание 5
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

**Сервер должен:**
- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

**Сервер:**
```python
import http.client
import socket
import sys
from datetime import datetime
from urllib.parse import unquote
import threading
import typing as tp

HOST = "localhost"
PORT = 8080


class Logger:
    def __init__(self, service: tp.Union[object, str] = None):
        self.__red = "\033[31m"
        self.__yellow = "\033[33m"
        self.__green = "\033[32m"
        self.__white = "\033[37m"
        self.__reset = "\033[0m"
        if service is None:
            print("Логгер инициализирован без имени.")
        if isinstance(service, object) and service is not None:
            self.__service_name = service.__class__.__name__
        elif isinstance(service, str):
            self.__service_name = service
        else:
            self.__service_name = "UnnamedService"

    def info(self, msg):
        print(f"[{self.__gettime()}] {self.__green}[INFO]{self.__reset} [{self.__service_name}]: {msg}")

    def warn(self, msg):
        print(f"[{self.__gettime()}] {self.__yellow}[WARN]{self.__reset} [{self.__service_name}]: {msg}")

    def error(self, msg):
        print(f"{self.__gettime()}] {self.__red}[ERROR]{self.__reset} [{self.__service_name}]: {msg}")

    def __gettime(self):
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')


grades_data = {}


class MyHTTPServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def serve_forever(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind((self._host, self._port))
            server.listen()
            server.settimeout(1)
            log.info(f"Сервер запущен на адресе {self._host}:{self._port}")
            while True:
                try:
                    conn, _ = server.accept()
                    client_thread = threading.Thread(target=self.serve_client, args=(conn,), daemon=True)
                    client_thread.start()
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    log.error(f"Что-то пошло не так: {e}")
        except KeyboardInterrupt:
            log.warn("Обнаружен ввод Ctrl+C")
        finally:
            log.info("Сервер останавливается...")
            server.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp, status_code = self.handle_request(req)
            self.send_response(conn, resp)
            self.log_request(req, status_code, http.client.responses[status_code])
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)
        if conn:
            conn.close()


    def parse_request(self, conn):
        rfile = conn.makefile('rb')

        request_line = rfile.readline().decode('iso-8859-1').strip()
        method, path, version = request_line.split()

        headers = self.parse_headers(rfile)

        content_length = int(headers.get('Content-Length', 0))
        body = rfile.read(content_length).decode('iso-8859-1') if content_length else None

        return {
            'method': method,
            'path': path,
            'version': version,
            'headers': headers,
            'body': body
        }

    def parse_headers(self, rfile):
        headers = {}
        while True:
            line = rfile.readline().decode('iso-8859-1').strip()
            if not line:
                break
            header_name, header_value = line.split(":", 1)
            headers[header_name.strip()] = header_value.strip()
        return headers

    def handle_request(self, req):
        if req['method'] == 'GET' and req['path'] == '/grades':
            return self.build_response(200, self.render_grades())
        elif req['method'] == 'POST' and req['path'] == '/submit':
            body = req['body']
            if body:
                params = dict(pair.split('=') for pair in body.split('&'))
                discipline = unquote(params.get('discipline', '')).strip()
                grade = unquote(params.get('grade', '')).strip()

                if discipline and grade:
                    grades_data[discipline] = grade
                    return self.build_response(200, self.render_submission_success())
            return self.build_response(400, "Invalid POST request")
        else:
            return self.build_response(404, "Not Found")

    def build_response(self, status_code, body):
        response_line = f"HTTP/1.1 {status_code} {http.client.responses[status_code]}\r\n"
        headers = "Content-Type: text/html; charset=utf-8\r\n"
        headers += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        headers += "Connection: close\r\n"
        headers += "\r\n"
        response = response_line + headers + body
        return response, status_code

    def send_response(self, conn, resp):
        conn.sendall(resp.encode('utf-8'))

    def send_error(self, conn, err):
        resp, _ = self.build_response(500, f"Error: {err}")
        self.send_response(conn, resp)
        conn.close()

    def render_submission_success(self):
        return """
        <html><head><meta charset="UTF-8"><title>Submission Success</title></head><body>
        <h2>Data submitted successfully!</h2>
        <button onclick="window.location.href='/grades'">Return to Grades</button>
        </body></html>
        """

    def render_grades(self):
        html = "<html><head><title>Зачётка</title></head><body>"
        html += "<h1>Зачётка</h1>"
        if grades_data:
            html += "<ul>"
            for discipline, grade in grades_data.items():
                html += f"<li>{discipline}: {grade}</li>"
            html += "</ul>"
        else:
            html += "В зачётке пусто. Почему бы это не исправить? ;)"
        html += "<h3>Добавить запись:</h3>"
        html += """
        <form method="POST" action="/submit">
            <label for="discipline">Дисциплина:</label>
            <input type="text" id="discipline" name="discipline"><br>
            <label for="grade">Оценка:</label>
            <input type="text" id="grade" name="grade"><br>
            <input type="submit" value="Сохранить">
        </form>
        """
        html += "</body></html>"
        return html

    def log_request(self, req, status_code, status_text):
        log_message = (f"Request: {req['method']} {req['path']} | "
                       f"Response: {status_code} {status_text}")
        log.info(log_message)


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 2 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT

    serv = MyHTTPServer(HOST, PORT)
    log = Logger(serv)
    serv.serve_forever()
```

