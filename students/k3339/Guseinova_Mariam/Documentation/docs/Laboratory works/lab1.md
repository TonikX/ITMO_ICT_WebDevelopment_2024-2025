# Лабораторная работа 1. Работа с сокетами.

## Задание 1.
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

* Обязательно использовать библиотеку socket.
* Реализовать с помощью протокола UDP.

Код client.py:
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)
    
# Отправка сообщения серверу
message = 'Hello, server'
client_socket.sendto(message.encode(), server_address)
print(f'Сообщение "{message}" отправлено серверу')
    
data, _ = client_socket.recvfrom(1024)
print(f'Ответ сервера: "{data.decode()}"')
    
client_socket.close()
```
Код server.py:
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)
server_socket.bind(server_address)

print('Сервер запущен')

while True:
    # Ожидание данных от клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f'Получено сообщение клиента: "{data.decode()}"')

    # Отправка ответа
    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
    print(f'Ответ "{response}" отправлен клиенту')
```

## Задание 2.
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Вариант 3: Поиск площади трапеции.

Код client.py:
```python
import socket

# Настройка TCP-клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)

client_socket.connect(server_address)

print("Для расчета площади трапеции введите несколько параметров:")

try:
    a = input('Длина первого основания (a): ')
    b = input('Длина второго основания (b): ')
    h = input('Высота (h): ')

    # Отправление данных на сервер
    message = f'{a} {b} {h}'
    client_socket.sendall(message.encode())

    data = client_socket.recv(1024).decode()
    print(f'Ответ сервера: {data}')

finally:
    client_socket.close()
```
Код server.py:
```python
import socket


def calculate_trapezoid_area(a, b, h):
    # Формула площади трапеции (вариант 11)
    return (a + b) * h / 2


# Настройка TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
server_socket.bind(server_address)
server_socket.listen(1)  # Ожидание подключения клиента

print('Сервер запущен')

while True:
    connection, client_address = server_socket.accept()
    try:
        print(f'Подключен клиент: {client_address}')

        # Получение данных от клиента
        data = connection.recv(1024).decode()
        if data:
            a, b, h = map(float, data.split())
            print(f'Получены параметры трапеции: a = {a}, b = {b}, h = {h}')

            area = calculate_trapezoid_area(a, b, h)

            response = f'Площадь трапеции равна: {area:.2f}'
            connection.sendall(response.encode())
            print(f'Ответ отправлен: {response}')
    finally:
        connection.close()
```
## Задание 3.
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Код server.py:
```python
import socket

# Наша HTML страничка
HTML_FILE = 'index.html'

# Настройка TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
server_socket.bind(server_address)
server_socket.listen(1)  # Ожидание одного клиента

print(f'Сервер запущен')

while True:
    connection, client_address = server_socket.accept()
    try:
        print(f'Подключен клиент: {client_address}')

        request = connection.recv(1024).decode()
        print(f'Запрос клиента:\n{request}')

        # Чтение HTML-файла
        try:
            with open(HTML_FILE, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Формирование HTTP-ответа
            response = (
                (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        f"Content-Length: {len(html_content)}\r\n"
                        "\r\n"
                        + html_content
                )
            )

        except FileNotFoundError:
            # Если файл не найден отправляем 404 ошикбу
            response = (
                'HTTP/1.1 404 Not Found\r\n\r\n'
                '<h1>404 Not Found</h1>'
            )

        connection.sendall(response.encode())

    finally:
        connection.close()
```
index.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Server</title>
</head>
<body>
    Welcome to the family, son
</body>
</html>
```

## Задание 4.
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:

* Обязательно использовать библиотеку `socket`.
* Для многопользовательского чата необходимо использовать библиотеку `threading`.

Реализация:

* Протокол TCP: 100% баллов.
* Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

Код client.py:
```python
import socket
import threading

# Настройка TCP-клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 9090)
client_socket.connect(server_address)


# Функция для получения сообщений от сервера
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == 'USERNAME':
                client_socket.send(username.encode())
            else:
                print(message)
        except:
            print('Ошибка при подключении к серверу.')
            client_socket.close()
            break


# Функция для отправки сообщений серверу
def send_messages():
    while True:
        message = f'{username}: {input("")}'
        client_socket.send(message.encode())


username = input('Введите ваше имя: ')

# Запуск потоков для отправки и получения сообщений
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
```
Код server.py:
```python
import socket
import threading

# Настройка TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 9090)
server_socket.bind(server_address)
server_socket.listen()

clients = []  # Хранение всех клиентов
usernames = []  # Хранение имен


# Широковещательная рассылка сообщения всем клиентам
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


# Обработка сообщений от клиентов
def handle_client(client):
    while True:
        try:
            # Получаем сообщение от клиента
            message = client.recv(1024)
            if message:
                broadcast(message)  # Пересылаем сообщение всем клиентам
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                username = usernames[index]
                broadcast(f'{username} покинул чат!'.encode())
                usernames.remove(username)
                break


# Функция для принятия новых подключений
def receive_connections():
    print("Сервер запущен и ожидает подключения пользователей")
    while True:
        client, address = server_socket.accept()
        print(f'Новое подключение: {address}')

        # Получаем и сохраняем имя пользователя
        client.send('USERNAME'.encode())
        username = client.recv(1024).decode()
        usernames.append(username)
        clients.append(client)

        print(f'Имя пользователя: {username}')
        # Сообщаем о новом пользователе
        client.send('Вы подключены к чату!\n'.encode())
        broadcast(f'{username} присоединился к чату!'.encode())

        # Запускаем поток для обработки сообщений от клиента
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


receive_connections()
```
## Задание 5.
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Задание:

Сервер должен:

* Принять и записать информацию о дисциплине и оценке по дисциплине.
* Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

Код server.py:
```python
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999

grade_list = []


class GradeHandler(BaseHTTPRequestHandler):
    def send_html_response(self, html_content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def do_GET(self):
        html = self.generate_html_page()
        self.send_html_response(html)

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8')
        data = parse_qs(post_body)

        discipline = data.get('subject', [''])[0]
        grade = data.get('score', [''])[0]

        if discipline and grade:
            self.record_grade(discipline, grade)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    def record_grade(self, discipline, grade):
        entry = next((rec for rec in grade_list if rec['subject'] == discipline), None)
        if entry:
            entry['score'] += f", {grade}"
        else:
            grade_list.append({'subject': discipline, 'score': grade})

    def generate_html_page(self):
        page = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Grade Tracker</title>
</head>
<body>
    <h1>Grades List</h1>
    <table border="1">
        <tr><th>Subject</th><th>Grades</th></tr>"""

        for rec in grade_list:
            page += f"<tr><td>{rec['subject']}</td><td>{rec['score']}</td></tr>"

        page += """
    </table>
    <h2>Add a Grade</h2>
    <form method="POST" action="/">
        <label for="subject">Subject:</label><br>
        <input type="text" id="subject" name="subject" required><br>
        <label for="score">Grade:</label><br>
        <input type="text" id="score" name="score" required><br><br>
        <input type="submit" value="Add">
    </form>
</body>
</html>"""
        return page


def start_server():
    address = (SERVER_HOST, SERVER_PORT)
    http_server = HTTPServer(address, GradeHandler)
    print(f"Server running at http://{SERVER_HOST}:{SERVER_PORT}")
    http_server.serve_forever()


if __name__ == '__main__':
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down server.")
```