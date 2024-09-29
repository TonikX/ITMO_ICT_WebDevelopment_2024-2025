# Задание 2

### Описание задачи

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры 
которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

* Теорема Пифагора.

### Реализация

##### Стэк
* Python: 3.10
* Библиотека: socket, math.

**Серверная часть:**
```
import math
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 65432))
sock.listen()
conn, addr = sock.accept()

with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        a, b = map(float, data.split())
        c = math.sqrt(a ** 2 + b ** 2)
        conn.sendall(f"{c}".encode('utf-8'))
```

**Клиентская часть:**
```
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 65432))
while True:
    a = input("Введите катет a: ")
    b = input("Введите катет b: ")
    if a == "exit" or b == "exit":
        break
    sock.sendall(f"{a} {b}".encode('utf-8'))
    data = sock.recv(1024).decode('utf-8')
    print(f"Гипотенуза: {data}")
```