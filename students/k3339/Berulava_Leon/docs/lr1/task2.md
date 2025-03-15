# Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

Теорема Пифагора.
Решение квадратного уравнения.
Поиск площади трапеции.
Поиск площади параллелограмма.
Порядок выбора варианта: Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола TCP.

## Код
Серверная часть
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 12345))
s.listen(1)

while True:
    conn, addr = s.accept()

    data = conn.recv(1024).decode('utf-8')
    a, b = data.split()
    a = int(a)
    b = int(b)
    pif = (a**2+b**2)**0.5

    conn.send(str(pif).encode())
    conn.close()

s.close()
```
Клиентская часть

```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

print("Введи два числа")
chislo = input()

client_socket.send(chislo.encode())

result = client_socket.recv(1024).decode()

print("Гипотенуза =", result)

client_socket.close()
```

