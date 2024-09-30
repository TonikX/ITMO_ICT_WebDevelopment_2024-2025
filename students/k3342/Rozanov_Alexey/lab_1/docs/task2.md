# Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры 
которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Операция: Поиск площади параллелограмма

Сервер рассчитывает площадь параллелограмма из двух сторон и угла между ними

## Файл server.py

Код:

```python
import socket
import math
import signal


def raise_timeout(signum, frame):
    """
    Функция для рейза ошибки таймаута
    :param signum:
    :param frame:
    :return:
    """
    raise TimeoutError


def handle_client(socket_user):
    """
    Client handler. Gets data from client
    and counts hippotenuse
    :param socket_user:
    :return:
    """
    user_data = socket_user.recv(1024).decode('utf-8')
    if not user_data:
        raise ValueError('The data is empty')

    try:
        a, b, alpha = map(float, user_data.split())
        result = round(a * b * math.sin(math.radians(alpha)), 2)
        socket_user.send(f"Square: {result}".encode('utf-8'))
    except ValueError:
        socket_user.send("Error: incorrect data".encode('utf-8'))
    finally:
        socket_user.close()


def start_server():
    """
    starting the server, waiting for client
    and using handle_client()
    :return:
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8088))
    server.listen(5)
    print("Server is up and ready")

    while True:
        socket_user, addr = server.accept()
        print(f"Client {addr} is connected")
        handle_client(socket_user)


if __name__ == "__main__":

    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(60)

    try:
        start_server()
    finally:
        signal.alarm(0)
```

Скриншоты работы:

[Скриншот работы сервера](imgs/task2_server.png)

## Файл client.py

Код:

```python
import socket


if __name__ == "__main__":
    socket_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8088)
    message = '2 4 30'

    socket_user.connect(server_address)
    socket_user.send(message.encode('utf-8'))

    resp = socket_user.recv(1024)

    print(resp.decode())

    socket_user.close()
```

Скриншоты работы:

[Скриншот работы клиента](imgs/task2_client.png)