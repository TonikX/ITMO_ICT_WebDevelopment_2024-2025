# Лабораторная работа №1
В данном README-файле представлен ход выполнения заданий по дисциплине «Web-программирование».

Работы выполнила Ефимова Валерия, группа К3344.

[Ссылка на файлы с кодом](https://github.com/valerieefim/ITMO_ICT_WebDevelopment_2024-2025/tree/main/students/k3344/Efimova_Valeriia/lr_1)

## Задание №1

Реализовать клиентскую и серверную часть приложения. Клиент отсылает серверу сообщение «Hello, server». Сообщение должно отразиться на стороне сервера. Сервер в ответ отсылает клиенту сообщение «Hello, client». Сообщение должно отобразиться у клиента.

- Использовать библиотеку socket.
- Реализовать с помощью протокола UDP.

## Выполнение

**Как работает сервер:**
```
import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Сервер готов к приему сообщений...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    
    print(f"Сообщение от клиента: {data.decode()}")
    
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
```

Сначала мы создаём сокет с параметрами AF_INET (IPv4) и SOCK_DGRAM (UDP), после чего привязываем его к адресу localhost и порту 12345. Затем сервер переходит в режим ожидания и постоянно прослушивает входящие сообщения от клиентов, принимая их с помощью функции recvfrom() и выводя на экран. После получения сообщения сервер отправляет ответ "Hello, client" обратно клиенту через sendto().

**Как работает клиент:**
```
import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)

message = "Hello, server"
client_socket.sendto(message.encode(), server_address)

data, _ = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

client_socket.close()
```
Сначала мы так же создаем сокет с параметрами AF_INET (для IPv4) и SOCK_DGRAM (для использования протокола UDP). Далее мы указываем адрес и порт сервера (localhost, 12345) и отправляем сообщение "Hello, server" с помощью функции sendto(). После этого мы ожидаем ответ от сервера, используя recvfrom(), принимаем данные и выводим их на экран. Завершаем работу клиента закрытием сокета с помощью close().

## Задание №2 (вариант а, теорема Пифагора)

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у сервера выполнение математической операции, параметры, которые вводятся с клавиатуры. Сервер обрабатывает полученные данные и возвращает результат клиенту.

- Обязательно использовать библиотеку socket
- Реализовать с помощью протокола TCP

## Выполнение

**Как работает сервер:**
```
import socket
import math


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1) 

print("Сервер запущен и ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключен клиент с адресом: {addr}")

    data = conn.recv(1024).decode()
    if not data:
        break

    a, b = map(float, data.split(','))

    c = math.sqrt(a**2 + b**2)
    
    conn.send(str(c).encode())

    print(f"Вычисленная гипотенуза: {c}")

    conn.close()
```
Мы написали код для TCP-сервера, который принимает соединения от клиентов и вычисляет гипотенузу по заданным катетам. Сначала мы создаем TCP-сокет с параметрами AF_INET (для IPv4) и SOCK_STREAM (для использования протокола TCP). Затем сервер привязывается к адресу localhost и порту 8080 и начинает ожидать подключения с помощью метода listen(). В цикле сервер принимает соединения от клиентов через accept(), выводит адрес подключившегося клиента и получает от него данные (длины катетов) с помощью recv(). После этого сервер разбивает полученные данные на два значения преобразует их в числа и вычисляет гипотенузу с помощью теоремы Пифагора. Результат (значение гипотенузы) отправляется обратно клиенту через send(). После обработки каждого клиента соединение закрывается, и сервер продолжает ждать новых подключений.

**Как работает клиент:**
```
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

a = input("Введите длину первого катета: ")
b = input("Введите длину второго катета: ")

client_socket.send(f"{a},{b}".encode())

data = client_socket.recv(1024).decode()
print(f"Гипотенуза: {data}")

client_socket.close()
```
Вначале мы создаем TCP-сокет с параметрами AF_INET (для IPv4) и SOCK_STREAM (для использования TCP-соединения). Затем устанавливаем соединение с сервером, работающим на адресе localhost и порту 8080, с помощью команды connect(). После этого клиент запрашивает у пользователя ввод длин двух катетов прямоугольного треугольника и отправляет их серверу с помощью send(). Клиент ожидает ответ от сервера, который рассчитывает гипотенузу, и получает его через recv(). Результат выводится на экран. После завершения взаимодействия клиент закрывает сокет с помощью close().

## Задание №3

Реализовать серверную часть приложения. Клиент подключается к серверу. В ответ клиент получает http-сообщение, содержащее html-страницу, которую сервер подгружает из файла index.html.

- Обязательно использовать библиотеку socket

## Выполнение

**Как работает сервер:**
```
import socket


content = open("index.html").read()

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(("127.0.0.1", 8081))
conn.listen()

while True:
    socket = conn.accept()[0]
    data = socket.recv(1024)
    response = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" + content
    socket.send(response.encode())
    socket.close()
```
В начале кода мы открываем файл index.html и считываем его содержимое для последующей отправки. Далее создаем TCP-сокет, используя параметры AF_INET (для работы с IPv4) и SOCK_STREAM (для использования TCP). Сокет привязывается к адресу 127.0.0.1 (локальный адрес) и порту 8081, после чего сервер начинает прослушивать входящие соединения с помощью функции listen(). Когда происходит подключение, мы принимаем его с помощью accept(), получаем данные от клиента через recv() и формируем ответ, соответствующий HTTP-протоколу: строка с кодом ответа 200 OK, заголовком Content-Type: text/html, указывающим на тип контента (HTML), и сами данные HTML-файла, которые мы считали ранее. После формирования ответа, сервер отправляет его клиенту через send() и закрывает соединение с помощью close().


**Как работает html:**
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Лабораторная работа Леры Еф</title>
</head>
<body>
    <h1>Привет, вы смотрите лабораторную работу Валерии Ефимовой!</h1>
    <p>Хорошего дня</p>
</body>
</html>
```
Вначале мы используем декларацию <!DOCTYPE html> для указания типа документа как HTML5. В теге <html> указываем, что язык страницы — английский (lang="en"). В секции <head> содержатся метаданные: кодировка страницы задана как UTF-8, что позволяет корректно отображать текст на разных языках. В секции <body> располагается основной контент страницы.

## Задание №4

Реализовать двухпользовательский или многопользовательский чат (реализован многопользовательский).

- Обязательно использовать библиотеку threading.

## Выполнение

**Как работает сервер:**
```
import socket
import threading


HOST = 'localhost'
PORT = 9090

clients = []

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ] {addr} подключился.")
    connected = True
    while connected:
        try:
            message = conn.recv(1024)
            if message:
                print(f"[{addr}] {message.decode()}")
                broadcast(message, conn)
            else:
                connected = False
        except:
            connected = False

    conn.close()
    clients.remove(conn)
    print(f"[ОТКЛЮЧЕНИЕ] {addr} отключился.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ЗАПУЩЕН] Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[АКТИВНЫЕ ПОДКЛЮЧЕНИЯ] {threading.active_count() - 1}")

start_server()
```
Каждый клиент добавляется в список clients, и его сообщения пересылаются другим подключенным пользователям через функцию broadcast(). В потоке для каждого клиента функция handle_client() обрабатывает получение сообщений и их пересылку, а при отключении клиента сокет закрывается. Сервер постоянно прослушивает новые подключения и запускает отдельный поток для каждого клиента, обеспечивая поддержку нескольких активных пользователей одновременно.


**Как работает клиент:**
```
import socket
import threading


HOST = 'localhost'
PORT = 9090

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

send_thread = threading.Thread(target=send_messages, args=(client_socket,))
send_thread.start()
```
Сначала создается сокет и устанавливается соединение с сервером на адресе localhost и порту 9090. Для получения сообщений от сервера используется функция receive_messages(), которая постоянно слушает сокет и выводит входящие сообщения на экран. Если сообщение не получено или возникает ошибка, цикл прерывается. Для отправки сообщений создается функция send_messages(), которая позволяет пользователю вводить текст и отправлять его на сервер. Для одновременного выполнения получения и отправки сообщений создаются два отдельных потока: один для функции receive_messages(), а другой для send_messages(), что обеспечивает эффективное взаимодействие с сервером в реальном времени.

## Задание №5

Необходимо написать простой web-сервер для обработки GET и POST http запросов средствами Python и библиотеки socket. Задание: сделать сервер, который может:
- принять и записать информацию о дисциплине и оценке по дисциплине.
- отдать информацию обо всех оценах по дсициплине в виде html-страницы.

## Выполнение

**Как работает сервер:**
```
import socket
import urllib.parse


grades_data = {}

def generate_html():
    html_content = """
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .content {
                display: flex;
            }
            .form {
                flex: 1;
            }
            .table {
                flex: 1;
                margin-left: 20px;
                border: 1px solid black;
                padding: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h1>Оценки по дисциплинам</h1>
        <div class="content">
            <div class="form">
                <form method='POST' action='/'>
                    <label>Дисциплина:</label> <input type='text' name='discipline' required><br><br>
                    <label>Оценка:</label> <input type='text' name='grade' required><br><br>
                    <input type='submit' value='Отправить оценку'><br><br>
                </form>
            </div>
            <div class="table">
                <h2>Список оценок</h2>
                <table>
                    <tr>
                        <th>Дисциплина</th>
                        <th>Оценка</th>
                    </tr>
    """
    
    for discipline, grade in grades_data.items():
        html_content += f"<tr><td>{discipline}</td><td>{grade}</td></tr>"
    
    html_content += """
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def handle_post_request(body):
    post_data = urllib.parse.parse_qs(body)
    discipline = post_data.get('discipline', [None])[0]
    grade = post_data.get('grade', [None])[0]

    print(f"POST данные: дисциплина = {discipline}, оценка = {grade}")

    if discipline and grade:
        grades_data[discipline] = grade
        print(f"Сохранено: {discipline} -> {grade}")

def handle_client_connection(client_socket):
    request_data = b''
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        request_data += data
        if b'\r\n\r\n' in request_data:
            break

    request_text = request_data.decode('utf-8')
    print(f"Получен запрос:\n{request_text}\n")

    if '\r\n\r\n' in request_text:
        headers_part, body = request_text.split('\r\n\r\n', 1)
    else:
        headers_part = request_text
        body = ''

    request_lines = headers_part.split('\r\n')
    request_line = request_lines[0]
    headers = {}
    for header_line in request_lines[1:]:
        if ': ' in header_line:
            key, value = header_line.split(': ', 1)
            headers[key] = value
    if request_line.startswith('POST'):
        content_length = int(headers.get('Content-Length', '0'))
        body_bytes = body.encode('utf-8')
        bytes_needed = content_length - len(body_bytes)
        while bytes_needed > 0:
            data = client_socket.recv(4096)
            body_bytes += data
            bytes_needed -= len(data)
        body = body_bytes.decode('utf-8')
        print(f"Тело POST-запроса: {body}")
        handle_post_request(body)

    response_body = generate_html()
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
        "\r\n"
        f"{response_body}"
    )

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8081))
    server_socket.listen(5)
    print("Сервер запущен на порту 8081...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключение от {addr}")
        handle_client_connection(client_socket)

start_server()   
```
Мы разработали простой HTTP-сервер, который принимает оценки по дисциплинам и отображает их в виде таблицы на веб-странице. В начале кода создается словарь grades_data, который хранит пары "дисциплина-оценка". Функция generate_html() формирует HTML-контент с формой для ввода дисциплины и оценки, а также таблицей для отображения уже введенных данных.

При обработке POST-запросов функция handle_post_request() извлекает дисциплину и оценку из данных запроса и сохраняет их в grades_data. Функция handle_client_connection() отвечает за прием входящих соединений, считывание данных запроса и их обработку. Если запрос является POST, она получает тело запроса, обрабатывает его и формирует ответ.

Сервер запускается на порту 8081 и ожидает подключения клиентов. При каждом новом подключении сервер создает отдельный сокет для обработки запроса, обеспечивая возможность ввода и отображения оценок в реальном времени.

## Вывод по лабораторной работе

В процессе выполнения лабораторной работы я овладела навыками работы с сокетами и поняла, как функционирует соединение между клиентом и сервером в целом. Также я изучила, как использовать потоки.