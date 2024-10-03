# Task 2

   Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у
сервера выполнение математической операции, параметры, которые вводятся с
клавиатуры. Сервер обрабатывает полученные данные и возвращает результат
клиенту. Вариант:

a. Теорема Пифагора

b. ***Решение квадратного уравнения.****

c. Поиск площади трапеции.

d. Поиск площади параллелограмма.

Вариант выбирается в соответствии с порядковым номером в журнале. Пятый
студент получает вариант 1 и т.д.
Обязательно использовать библиотеку socket
Реализовать с помощью протокола TCP

server.py
```python
import socket
import math


def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Два корня: {root1} и {root2}"
    elif discriminant == 0:
        root = -b / (2 * a)
        return f"Один корень: {root}"
    else:
        return "Действительных корней нет"


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    data = client_connection.recv(1024).decode()
    if not data:
        break

    a, b, c = map(float, data.split())
    result = solve_quadratic(a, b, c)

    client_connection.send(result.encode())
    print(f'Отправлен результат: {result}')

    client_connection.close()

```
client.py
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

a = float(input("Введите коэффициент a: "))
b = float(input("Введите коэффициент b: "))
c = float(input("Введите коэффициент c: "))

message = f"{a} {b} {c}"
client_socket.send(message.encode())

result = client_socket.recv(1024).decode()
print(f"Решение уравнения: {result}")

client_socket.close()

```
