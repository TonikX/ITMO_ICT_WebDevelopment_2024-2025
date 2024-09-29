### Задание

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции (теорема Пифагора), параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту. Реализовать TCP соединение.
### `server.py`

```python
import socket
import math


def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        a, b = map(float, data.split())

        if a <= 0 or b <= 0:
            raise Exception
        c = math.sqrt(a ** 2 + b ** 2)

        client_socket.sendall(f"Гипотенуза: {c:.2f}".encode())
    except Exception as e:
        client_socket.sendall(f"Ошибка: {str(e)}".encode())
    finally:
        client_socket.close()


def start_server(host='127.0.0.1', port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Подключен клиент: {addr}")
        handle_client(client_socket)


if __name__ == "__main__":
    start_server()
```

### `client.py`

```python
import socket


def start_client(host='127.0.0.1', port=65432):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))

        a = input("Введите длину первого катета: ")
        b = input("Введите длину второго катета: ")

        client.sendall(f"{a} {b}".encode())

        result = client.recv(1024).decode()
        print(f"Ответ от сервера: {result}")

    finally:
        client.close()


if __name__ == "__main__":
    start_client()
```

Сервер создает сокет, работающий по протоколу TCP и ожидает сообщение от клиента. Клиент аналогично создает сокет, отправляет на адрес сервера сообщение с катетами треугольника и ожидает ответа. Сервер валидирует полученные данные, высчитывает гипотенузу и возвращает результат.