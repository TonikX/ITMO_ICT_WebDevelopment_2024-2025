### Задание 2:

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

- Теорема Пифагора.
- Решение квадратного уравнения.
- Поиск площади трапеции.
- Поиск площади параллелограмма.

Требования:

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.

### Ход работы:

#### server.py

```
import socket
import math


def calculate_pythagorean(a, b):
    return math.sqrt(a ** 2 + b ** 2)


def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return "No real roots"
    elif discriminant == 0:
        x = -b / (2 * a)
        return x
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return x1, x2


def calculate_trapezoid_area(a, b, h):
    return ((a + b) / 2) * h


def calculate_parallelogram_area(base, height):
    return base * height


def handle_client_request(data):
    operation, *args = data.split()
    args = list(map(float, args))
    if operation == 'pythagorean':
        return calculate_pythagorean(*args)
    elif operation == 'quadratic':
        return solve_quadratic(*args)
    elif operation == 'trapezoid_area':
        return calculate_trapezoid_area(*args)
    elif operation == 'parallelogram_area':
        return calculate_parallelogram_area(*args)
    else:
        return "Invalid operation"


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Server listening on port 8080...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        result = handle_client_request(data)
        conn.sendall(str(result).encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    start_server()

```


#### client.py

```
import socket


def get_input():
    operation = input("Enter operation (pythagorean, quadratic, trapezoid_area, parallelogram_area): ").strip()
    if operation == 'pythagorean':
        a = float(input("Enter side a: "))
        b = float(input("Enter side b: "))
        return f"{operation} {a} {b}"
    elif operation == 'quadratic':
        a = float(input("Enter coefficient a: "))
        b = float(input("Enter coefficient b: "))
        c = float(input("Enter coefficient c: "))
        return f"{operation} {a} {b} {c}"
    elif operation == 'trapezoid_area':
        a = float(input("Enter base1 (a): "))
        b = float(input("Enter base2 (b): "))
        h = float(input("Enter height (h): "))
        return f"{operation} {a} {b} {h}"
    elif operation == 'parallelogram_area':
        base = float(input("Enter base: "))
        height = float(input("Enter height: "))
        return f"{operation} {base} {height}"
    else:
        return "Invalid operation"


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    request = get_input()
    client_socket.sendall(request.encode('utf-8'))
    response = client_socket.recv(1024)
    print(f"Result: {response.decode('utf-8')}")

    client_socket.close()


if __name__ == "__main__":
    start_client()
```

Для успешного обмена данными сначала необходимо запустить серверный файл, который всегда готов 
слушать, а затем клиентский файл, который сразу после установки соединения отправляет стороны 
треугольника. Сервер принимает стороны треугольника и выполняет поиск гипотенузы, предварительно 
проверив положительность сторон.

TCP соединение обеспечивается созданием TCP-socket с помощью параметра `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
