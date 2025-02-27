# Задание 2

## TCP Клиент-Сервер с математической операцией

### Краткое описание задания

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у сервера вычисление гипотенузы по теореме
Пифагора, вводя стороны треугольника. Сервер обрабатывает запрос и возвращает результат.

### Как запускать

1. Запустите сервер:

``` bash
python task2/tcp_server_math.py
```
2. Запустите клиента:

``` bash
python task2/tcp_client_math.py
```

### Сервер

``` python 
import socket
import threading
import math

def tcp_server_math():
    def handle_client(client_socket):
        try:
            operation = client_socket.recv(1024).decode()
            if operation == "1":  # Теорема Пифагора
                a = float(client_socket.recv(1024).decode())
                b = float(client_socket.recv(1024).decode())
                result = math.sqrt(a ** 2 + b ** 2)
                client_socket.sendall(str(result).encode())
            elif operation == "2":  # Квадратное уравнение
                a = float(client_socket.recv(1024).decode())
                b = float(client_socket.recv(1024).decode())
                c = float(client_socket.recv(1024).decode())
                discriminant = b ** 2 - 4 * a * c
                if discriminant >= 0:
                    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                    result = f"Корни: {root1}, {root2}"
                else:
                    result = "Нет действительных корней"
                client_socket.sendall(result.encode())
        finally:
            client_socket.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 23456))
    server_socket.listen(5)
    print("TCP сервер запущен на порту 23456")

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    tcp_server_math()
```

### Клиент

``` python
import socket
import threading
import math

def tcp_client_math():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 23456))
    print("Выберите операцию: 1 - Теорема Пифагора, 2 - Квадратное уравнение")
    operation = input("Введите номер операции: ")
    client_socket.sendall(operation.encode())

    if operation == "1":
        a = input("Введите сторону a: ")
        b = input("Введите сторону b: ")
        client_socket.sendall(a.encode())
        client_socket.sendall(b.encode())
    elif operation == "2":
        a = input("Введите коэффициент a: ")
        b = input("Введите коэффициент b: ")
        c = input("Введите коэффициент c: ")
        client_socket.sendall(a.encode())
        client_socket.sendall(b.encode())
        client_socket.sendall(c.encode())

    result = client_socket.recv(1024).decode()
    print(f"Результат: {result}")
    client_socket.close()
if __name__ == '__main__':
    tcp_client_math()
```