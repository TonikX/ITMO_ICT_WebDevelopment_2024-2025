---
title: Лабораторная работа — Сокеты и Web-приложения  
author: [Твоё имя]  
date: [Дата]  
---

# Введение  
В этой работе выполняется 5 заданий по сетевому программированию: UDP, TCP, HTTP, чат, работа с GET/POST. Цель — закрепить навыки работы с `socket`, потоками и HTTP.

# Содержание  
1. Задание 1 — UDP Hello  
2. Задание 2 — TCP + Математика  
3. Задание 3 — HTTP + index.html  
4. Задание 4 — Чат  
5. Задание 5 — Веб-журнал оценок (GET/POST)  
6. Вывод

---

## Задание 1 — UDP Hello  
**Условие:**  
Клиент отправляет «Hello, server», сервер получает и показывает, потом отвечает «Hello, client», и клиент показывает ответ. Протокол: UDP.  

**Код (сервер):**  
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # создаём UDP сокет

sock.bind(("127.0.0.1", 12345)) # привязываем его к локальному адресу и порту

print("UDP сервер запущен и ждёт сообщений...")

while True:
    data, addr = sock.recvfrom(1024)  # ждём сообщение от клиента, 1024 — максимальный размер пакета

    print("Получено:", data.decode(), "от", addr)

    sock.sendto("Hello, client".encode(), addr) # отвечаем клиенту
```
**Код (клиент):**  
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12345)

sock.sendto("Hello, server".encode(), server_address) # отправляем сообщение серверу

data, _ = sock.recvfrom(1024)
print("Ответ сервера:", data.decode())

sock.close()
```
![скрин работы](/Users/nastasamelnikova/PycharmProjects/pythonProject9/telegram-cloud-photo-size-2-5379683809869560386-y.jpg)
![](/Users/nastasamelnikova/PycharmProjects/pythonProject9/telegram-cloud-photo-size-2-5379683809869560482-y.jpg)

## Задание 2 —  TCP + Математика
 
**Условие:**  
Клиент вводит параметры, сервер делает одну из математических операций (например, теорему Пифагора). Протокол: TCP.

**Код (сервер):**  
```python
import socket
import math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаём TCP сокет

sock.bind(("127.0.0.1", 12345)) # привязываем к адресу и порту

sock.listen(1) # 1 = сколько подключений в очереди

print("TCP сервер ждёт подключение...")

conn, addr = sock.accept()
print("Подключился:", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break  # если клиент закрыл соединение — выходим

    try:
        a, b = map(float, data.split())
        c = math.sqrt(a**2 + b**2)  # считаем гипотенузу
        conn.send(str(c).encode())  # отправляем обратно
    except:
        conn.send("Ошибка ввода!".encode())

conn.close()
```
**Код (клиент):**
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаём TCP сокет

sock.connect(("127.0.0.1", 12345)) # подключаемся к серверу

a = input("Введите a: ")
b = input("Введите b: ")

sock.send((a + " " + b).encode()) # отправляем строку "a b"

result = sock.recv(1024).decode() # ждём результат
print("Результат:", result)

sock.close()
```
![скрин работы](/Users/nastasamelnikova/PycharmProjects/pythonProject9/telegram-cloud-photo-size-2-5379683809869560514-y.jpg)
![](/Users/nastasamelnikova/PycharmProjects/pythonProject9/telegram-cloud-photo-size-2-5379683809869560515-y.jpg)

## Задание 3 - HTTP + index.html  
**Условие:**  
Сервер отдаёт HTML-страницу, которую он читает из файла index.html.

**Код (сервер):**  
```python
import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8081))
sock.listen(1)

print("HTTP сервер ждёт подключение на http://127.0.0.1:8081/ ...")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print("Запрос:\n", request)

    try:
        path = request.split(" ")[1]
    except:
        path = "/"

    if path == "/":
        path = "/index.html"

    file_path = path.lstrip("/")

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        if file_path.endswith(".html"):
            content_type = "text/html"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            content_type = "image/jpeg"
        else:
            content_type = "application/octet-stream"

        response = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n".encode() + content
    else:
        response = "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nФайл не найден".encode()

    conn.send(response)
    conn.close()
```
**index.html**
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Мой первый сервер на Python</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #87CEFA;
            color: #000;
            text-align: center;
        }
        header {
            background: #4682B4;
            color: white;
            padding: 20px;
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        main {
            margin: 40px auto;
            max-width: 600px;
            background: #f0f8ff;
            color: #000;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 36px;
            margin-bottom: 20px;
            color: #000080;
        }
        img {
            max-width: 300px;
            margin-top: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.4);
        }
        .caption {
            margin-top: 10px;
            font-size: 16px;
            font-style: italic;
            color: #333;
        }
        footer {
            margin-top: 40px;
            padding: 15px;
            font-size: 14px;
            background: #4682B4;
            color: white;
        }
    </style>
</head>
<body>
    <header>
        Сервер
    </header>
    <main>
        <h1>DU-DU-DU</h1>
        <img src="verstappen_sid.jpg" alt="Sid Verstappen">
        <div class="caption">33 Verstappen </div>
    </main>
</body>
</html>
```
![скрин работы](/Users/nastasamelnikova/PycharmProjects/pythonProject9/telegram-cloud-photo-size-2-5379683809869560522-y.jpg)

## Задание 4 — Чат
**Условие:**
Многопользовательский чат через TCP с использованием потоков.
**Код (сервер):**
```python
import socket
import threading

clients = {}  # словарь: conn -> имя

def handle_client(conn, addr):
    try:
        nickname = conn.recv(1024).decode("utf-8", errors="ignore") # первым делом получаем ник от клиента
        clients[conn] = nickname
        print(f"[+] {nickname} подключился с {addr}")

        broadcast(f"📢 {nickname} вошёл в чат", conn) # рассылаем всем сообщение о подключении

        while True:
            msg = conn.recv(1024).decode("utf-8", errors="ignore")
            if not msg:
                break
            print(f"[{nickname}]: {msg}")
            broadcast(f"[{nickname}]: {msg}", conn)

    except:
        pass
    finally:
        if conn in clients: # отключение клиента
            name = clients[conn]
            print(f"[-] {name} отключился")
            broadcast(f"📢 {name} покинул чат", conn)
            del clients[conn]
        conn.close()

def broadcast(message, sender_conn=None):
    """Рассылка всем клиентам, кроме отправителя"""
    for c in list(clients.keys()):
        if c != sender_conn:
            try:
                c.send(message.encode("utf-8", errors="ignore"))
            except:
                c.close()
                del clients[c]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 12345))
sock.listen()

print("Сервер чата запущен...")

while True:
    conn, addr = sock.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
```
**Код (клиент):**
```python
import socket
import threading

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8", errors="ignore")
            if msg:
                print(msg)
            else:
                break
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 12345))

nickname = input("Введите свой ник: ") # спрашиваем имя
sock.send(nickname.encode("utf-8", errors="ignore"))

thread = threading.Thread(target=receive, args=(sock,)) # запускаем поток для приёма сообщений
thread.start()

print("Теперь можно писать сообщения")
while True:
    msg = input()
    sock.send(msg.encode("utf-8", errors="ignore"))
```
![скрин работы](/Users/nastasamelnikova/PycharmProjects/pythonProject9/telegram-cloud-photo-size-2-5379683809869560549-y.jpg)

## Задание 5 — Веб-журнал с оценками (GET / POST)
**Условие:**
Сервер принимает через POST дисциплину + оценку, хранит их, а при GET отдаёт HTML с журналом оценок по предметам.
Код (сервер с объединением оценок):

```python
import socket
from urllib.parse import parse_qs

grades = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8082))  # порт 8082
sock.listen(1)

print("Сервер запущен на http://127.0.0.1:8082/")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode("utf-8", errors="ignore")
    print("Запрос:\n", request)

    if request.startswith("POST"):
        body = request.split("\r\n\r\n", 1)[1]
        data = parse_qs(body)

        subject = data.get("subject", ["Неизвестно"])[0]
        grade = data.get("grade", ["-"])[0]

        if subject not in grades:
            grades[subject] = []
        grades[subject].append(grade)

        response_body = f"""
        <div class="container">
            <h2> Добавлено: {subject} — {grade}</h2>
            <a href="/">Назад</a>
        </div>
        """

    else:  # GET-запрос
        response_body = "<div class='container'><h1> Журнал оценок</h1><table>"
        response_body += "<tr><th>Дисциплина</th><th>Оценки</th></tr>"

        for subject, grade_list in grades.items():
            grades_str = ", ".join(grade_list)
            response_body += f"<tr><td><b>{subject}</b></td><td>{grades_str}</td></tr>"

        response_body += "</table>"

        response_body += """
        <h2>➕ Добавить новую оценку</h2>
        <form method="POST">
            <label>Дисциплина:</label><br>
            <input type="text" name="subject" style="width:300px; padding:5px;"><br><br>
            <label>Оценка:</label><br>
            <input type="text" name="grade" style="width:100px; padding:5px;"><br><br>
            <input type="submit" value="Добавить" 
                style="padding:10px 20px; background:#4682B4; color:white; border:none; border-radius:5px; cursor:pointer;">
        </form>
        </div>
        """

    page = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Журнал оценок</title>
        <style>
            body {{
                background: #87CEFA; /* голубой фон */
                font-family: Arial, sans-serif;
                color: #000;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            .container {{
                background: #f0f8ff;
                padding: 30px;
                border-radius: 15px;
                width: 600px;
                text-align: center;
                box-shadow: 0 0 20px rgba(0,0,0,0.3);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #4682B4;
                padding: 10px;
                text-align: center;
            }}
            th {{
                background: #4682B4;
                color: white;
            }}
        </style>
    </head>
    <body>
        {response_body}
    </body>
    </html>
    """

    response = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" + page
    conn.send(response.encode("utf-8"))
    conn.close()
```
![скрин работы](/Users/nastasamelnikova/PycharmProjects/pythonProject9/telegram-cloud-photo-size-2-5379683809869560559-y.jpg)

# Вывод 
В ходе выполнения лабораторной работы были изучены основные приёмы работы с сетевыми протоколами и библиотекой socket в Python. 
**На практических заданиях были реализованы:**
- простейшее взаимодействие по протоколу UDP (обмен сообщениями без установки соединения),
- клиент-серверное приложение на основе TCP с реализацией математических операций,
- HTTP-сервер, обслуживающий статическую страницу index.html,
- многопользовательский чат с потоками, позволяющий общаться нескольким клиентам одновременно,
- веб-журнал оценок, в котором данные обрабатываются через GET и POST-запросы и выводятся в структурированном виде.
**Выполненная работа позволила:**
- понять различия между протоколами UDP и TCP;
- освоить структуру и обработку HTTP-запросов вручную;
- закрепить навыки работы с многопоточностью в Python;
- научиться хранить и отображать данные в динамическом веб-приложении.
Таким образом, в рамках лабораторной работы удалось не только реализовать все требуемые задания, но и сформировать целостное представление о принципах работы клиент-серверных приложений и их взаимодействии через сетевые протоколы.


