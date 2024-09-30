# Задание 2
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

```Решение квадратного уравнения.```
### Требования:
- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.
---
### server.py
```python
import socket
import math

def equation_solution(a, b, c):
    d = b ** 2 - 4 * a * c
    if d < 0:
        return "No roots"
    elif d == 0:
        root = -b / (2 * a)
        return f"One root: {root}"
    else:
        root1 = (-b + math.sqrt(d)) / (2 * a)
        root2 = (-b - math.sqrt(d)) / (2 * a)
        return f"Two roots: {root1}, {root2}"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(4)

while True:
    clientsocket, address = server.accept()
    data = clientsocket.recv(1024).decode('utf-8')
    a, b, c = map(float, data.split(','))
    result = equation_solution(a, b, c)
    clientsocket.send(result.encode('utf-8'))
    clientsocket.close()
```
### client.py
```python
import socket

a = input("a:")
b = input("b:")
c = input("c:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))

client.send(f"{a},{b},{c}".encode('utf-8'))
result = client.recv(1024).decode('utf-8')
print(f"Solution: {result}")

client.close()
```
