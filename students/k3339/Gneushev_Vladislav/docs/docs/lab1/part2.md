
## Задание

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## Решение

Реализованная математическая операция: теорема Пифагора

## Как запустить

Клиент: Зайти в папку `lab1/part2` и запустить командой `python client.py`

Сервер: Зайти в папку `lab1/part2` и запустить командой `python server.py`


## Код
### Код клиента

```
import socket
from contextlib import contextmanager

from constants import SERVER_HOST, SERVER_PORT


@contextmanager
def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    try:
        yield sock
    finally:
        sock.close()


def send_message(sock, message: str):
    sock.send(message.encode("utf-8"))


def receive_message(sock):
    data = sock.recv(1024)
    return data.decode("utf-8")


def main():
    with client() as c:
        while True:
            message = input("Enter message: ")
            send_message(c, message)
            response = receive_message(c)
            print("Server response: " + response)


if __name__ == "__main__":
    main()
```


### Код сервера

```
import socket

from constants import SERVER_HOST, SERVER_PORT
from pythagorean import parse_pythagorean_params, calculate_pythagorean


def receive_message(conn):
    try:
        data = conn.recv(1024)
        udata = data.decode("utf-8")
        if not udata:
            return None
        print(f"Received message: {udata}")
        return udata
    except socket.timeout:
        return None


def send_message(conn, message: str):
    conn.sendall(message.encode("utf-8"))
    print(f"Sent message: {message}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen()
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with conn:
        while True:
            conn.settimeout(1.0)
            message = receive_message(conn)
            if message:
                try:
                    pythagorean_params = parse_pythagorean_params(message)
                except ValueError:
                    response = "Invalid input"
                else:
                    response = str(calculate_pythagorean(pythagorean_params))
                send_message(conn, response)
```

### Расчет по теореме Пифагора
```
from dataclasses import dataclass


@dataclass
class PythagoreanParams:
    a: int
    b: int


def parse_pythagorean_params(data: str) -> PythagoreanParams:
    ints_in_string = list(map(int, data.split()))
    if len(ints_in_string) != 2:
        raise ValueError("Expected two integers")

    return PythagoreanParams(
        a=ints_in_string[0],
        b=ints_in_string[1]
    )


def calculate_pythagorean(params: PythagoreanParams) -> float:
    return (params.a ** 2 + params.b ** 2) ** 0.5

```