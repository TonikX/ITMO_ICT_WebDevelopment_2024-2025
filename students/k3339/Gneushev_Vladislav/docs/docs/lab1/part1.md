
## Задание

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.


## Как запустить

Клиент: Зайти в папку `lab1/part1` и запустить командой `python client.py`

Сервер: Зайти в папку `lab1/part1` и запустить командой `python server.py`

## Код:
### Код клиента:

```
import socket
from contextlib import contextmanager

from constants import SERVER_HOST, SERVER_PORT


@contextmanager
def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    try:
        yield sock
    finally:
        sock.close()


def send_message(sock, message: str):
    sock.sendall(message.encode("utf-8"))


def receive_message(sock):
    data = sock.recv(1024)
    udata = data.decode("utf-8")
    return udata


def main():
    with client() as c:
        send_message(c, "Hello, server!")
        message = receive_message(c)
        print("Server response: " + message)


if __name__ == "__main__":
    main()

```


### Код сервера:

```
import socket

from constants import SERVER_HOST, SERVER_PORT


RESPONSES = {
    "Hello, server!": "Hello, client!",
}


def receive_message(sock):
    try:
        data, addr = sock.recvfrom(1024)
        udata = data.decode("utf-8")
        print(f"Received message from {addr}: {udata}")
        return udata, addr
    except socket.timeout:
        return None, None


def send_message(sock, message: str, addr):
    sock.sendto(message.encode("utf-8"), addr)
    print(f"Sent message to {addr}: {message}")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.settimeout(1.0)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        message, addr = receive_message(s)
        if message:
            response = RESPONSES.get(message, "Unknown message")
            send_message(s, response, addr)

```