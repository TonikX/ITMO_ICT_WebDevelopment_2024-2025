# Задание 2

## Описание

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Вариант 11 = Вариант 3 = Площадь трапеции

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: TCP

## Как запускать

1. Сервер:

   Листинг:
```python
import socket


def area(a, b, h):
    return (a + b) / 2 * h


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(("127.0.0.1", 2000))

print("Server started!")

serv.listen()

while True:
    sock, _ = serv.accept()
    data = sock.recv(1024).decode()
    a, b, h = data.split(',')
    sock.sendall(str(area(float(a), float(b), float(h))).encode())
```

 ```bash
 python3 server.py
 ```

2. Клиент:

   Листинг:

```python
import socket

print("Area of trapezoid")
a = input("A = ")
b = input("B = ")
h = input("H = ")

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect(("127.0.0.1", 2000))
serv.sendall(f'{a},{b},{h}'.encode())
data = serv.recv(1024)

print("Calculated S = ", data.decode())
```

   Запуск:
```bash
python3 client.py
```
   Далее требуется ввести длины оснований трапеции и ее высоту.