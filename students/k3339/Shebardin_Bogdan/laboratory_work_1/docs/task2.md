
---

## 📄 `docs/task2.md` — TCP, теорема Пифагора

# Задание 2. Вычисления через TCP

## Постановка

Клиент запрашивает математическую операцию, параметры вводятся с клавиатуры. Сервер вычисляет и возвращает результат.

**Вариант:**  Площадь трапеции —  `S=h(a+b)/2`.

**Требования:**
- Библиотека `socket`
- Протокол TCP

## Архитектура

TCP гарантирует доставку и порядок байт. Клиент вызывает `connect()`, сервер — `accept()`.

## Код сервера `server_for_task2.py`

```python
import socket

new_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
new_socket.bind(('localhost',8080))
new_socket.listen(5)
print("server was started")
conn, addr = new_socket.accept()
print("connected:", addr)


message = "выберете дейстриве: 1. площадь трапеции"
message2 = "напишите верхнее, нижнее основания и высоту через пробел"

while True:
    conn.send(message.encode("utf-8"))
    data = conn.recv(1024)
    data = data.decode("utf-8")
    if data != "1" or not data:
        break
    conn.send(message2.encode("utf-8"))
    answer = conn.recv(1024)
    answer = answer.decode("utf-8")
    x = int(answer.split(" ")[0])
    y = int(answer.split(" ")[1])
    z = int(answer.split(" ")[2])
    result = ((x+y)/2)*z
    print(result)
    conn.send(str(result).encode("utf-8") + b'\n')

conn.close()
```

## Код клиента `client_for_task2.py`

```python
import socket

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.connect(('localhost', 8080))

data = socket_server.recv(1024)
print(data.decode("utf-8"))

message = input()

socket_server.send(message.encode("utf-8"))
data = socket_server.recv(1024)
print(data.decode("utf-8"))
message = input()
socket_server.send(message.encode("utf-8"))
data = socket_server.recv(1024)
print(data.decode("utf-8"))

socket_server.close()
```
## Результат
Терминал 1 (клиент)
```text
выберете дейстриве: 1. площадь трапеции
1
напишите верхнее, нижнее основания и высоту через пробел
3 4 2
7.0
```
Терминал 2 (сервер)
```text
server was started
connected: ('127.0.0.1', 53259)
7.0
```
