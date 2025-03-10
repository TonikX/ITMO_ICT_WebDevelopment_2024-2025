# Отчет по Лабораторной работе №1

## Задание 1

### Текст задачи

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Листинг кода

#### Сервер

```
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Socket created')

# Привязываем сокет к адресу и порту
HOST = 'localhost'
PORT = 8080
s.bind((HOST, PORT))
print('Socket bind complete')

while True:
    message, address = s.recvfrom(1024)
    print(f"New message from client: {message.decode()}")

    response = 'Hello, UDP Client!'
    s.sendto(response.encode(), address)
    print(f"Message sent to client: {response}")
```

#### Клиент

```
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = 'localhost'
PORT = 8080
address = HOST, PORT
message = "Hi, UDP server!"

s.sendto(message.encode(), address)
print(f"Sent message to server: {message}")

response, server_address = s.recvfrom(1024)
print(f"Got reply from server: {response.decode()}")
s.close()
```

## Задание 2

### Текст задачи

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции (теорема пифагора), параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

### Листинг кода

#### Сервер

```
import socket
from math import sqrt


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 8081
address = HOST, PORT
s.bind(address)
s.listen(1)
print("Server is running!")
while True:
    client_connection, client_address = s.accept()
    print("We got connection now")
    request = client_connection.recv(1024).decode()
    try:
        a, b = map(float, request.split(','))
        if a > 0 and b > 0:
            result = str(sqrt(a**2 + b**2))
        else:
            result = "Invalid data"
    except:
        result = "Invalid data"

# Отправили ответ
    client_connection.sendall(result.encode())
    client_connection.close()

```

#### Клиент

```
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8081))

# Отправляем сообщение серверу
sides = input("Enter lengths of a and b: ")
client_socket.sendall(sides.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Server response: {response.decode()}')

# Закрываем соединение
client_socket.close()

```

## Задание 3

### Текст задачи

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Листинг кода

#### Сервер

```
import socket


HOST = 'localhost'
PORT = 8082
# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(50)
print(f"HTTP сервер запущен на http://{HOST}:{PORT}...")

# HTML-страница, которая будет отображаться в браузере
html_content = open("index.html", "r", encoding="utf-8").read()

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    # Формируем HTTP-ответ с заголовками и HTML-контентом
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    # Отправляем HTTP-ответ клиенту
    client_connection.sendall(http_response.encode())

    client_connection.close()
```

#### HTML страница

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web-programming</title>
</head>
<body>
    <h1>Цой Степан K3340</h1>
    <p> We got new connection!</p>
</body>
</html>
```

## Задание 4

### Текст задачи

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

### Листинг кода

#### Сервер

```
import socket
import threading

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"пользователь {client_address}:")
            print(message)
            if message:
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break


def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message.encode('utf-8'))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12366))
server_socket.listen(5)

print("Многопользовательский чат запущен...")

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Подключился {client_address}")

    threading.Thread(target=handle_client, args=(client_socket,)).start()
```

#### Клиент

```
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            client_socket.close()
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12366))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

print("Подключение к серверу установлено. Введите сообщение:")
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
```

## Задание 5

### Текст задачи

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.
Сервер должен:

- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Листинг кода

```
import socket
from urllib.parse import unquote_plus

grades = []
#Генерация html по данным из массива grades
def generate_html():
    html = "<html><head><meta charset='UTF-8'><title>Оценки по дисциплинам</title></head><body>"
    html += "<h1>Оценки по дисциплинам</h1><ul>"
    subjects = {}
    for grade in grades:
        subject = grade['subject']
        score = grade['score']
        if subject in subjects:
            subjects[subject].append(score)
        else:
            subjects[subject] = [score]

    # Вывод оценок
    for subject, scores in subjects.items():
        html += f"<li>{subject}: {', '.join(scores)}</li>"
    html += "</ul>"
    html += '''
        <h2>Добавить оценку</h2>
        <form method="POST">
            <label>Дисциплина: <input type="text" name="subject"></label><br>
            <label>Оценка: <input type="text" name="score"></label><br>
            <input type="submit" value="Добавить">
        </form>
    '''
    html += "</body></html>"
    return html

def parse_post_data(data):
    post_data = {}
    params = data.split('&')
    for param in params:
        key, value = param.split('=')
        post_data[key] = unquote_plus(value)
    return post_data

def handle_request(request):
    headers, _, body = request.partition('\r\n\r\n')
    lines = headers.splitlines()
    request_line = lines[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n' + response_body
        return response

    elif method == 'POST':
        post_data = parse_post_data(body)
        grades.append({'subject': post_data.get('subject', ''), 'score': post_data.get('score', '')})
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n' + response_body
        return response

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = 'localhost'
    PORT = 8084
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на порту http://{HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Получен запрос от {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        if request:
            response = handle_request(request)
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()

if __name__ == '__main__':
    start_server()

```
