# Задание:
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у
сервера выполнение математической операции, параметры, которые вводятся с
клавиатуры. Сервер обрабатывает полученные данные и возвращает результат
клиенту. Вариант - Поиск площади трапеции

## Требования:

- Обязательно использовать библиотеку socket.

- Реализовать с помощью протокола TCP.

## Клиент:
```py
from socket import socket, AF_INET, SOCK_STREAM


with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect(("localhost", 8080))
    client_socket.sendall(
        input(
            "Введите длины двух смежных сторон и высоту через пробел "
        ).encode()
    )
    data = client_socket.recv(1024)
    print("Ответ сервера: ", data.decode("utf-8"))

```

## Сервер:
```py
from socket import socket, AF_INET, SOCK_STREAM


def trapezoid_area(a, b, h):
    return 0.5 * (a + b) * h


with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", 8080))
    server_socket.listen()
    with server_socket.accept()[0] as client_socket:
        data = client_socket.recv(1024).decode()
        ans = trapezoid_area(*[int(x) for x in data.split()])
        client_socket.sendall(str(ans).encode())
```
