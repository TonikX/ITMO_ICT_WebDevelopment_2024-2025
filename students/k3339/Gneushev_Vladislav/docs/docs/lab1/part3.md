## Задание

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.


## Как запустить

Клиент: Зайти в папку `lab1/part3` и запустить командой `python client.py`

Сервер: Зайти в папку `lab1/part3` и запустить командой `python server.py`

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


### Код сервера

```
import socket
from constants import SERVER_HOST, SERVER_PORT


def get_html():
    with open("static/index.html", "r") as f:
        return f.read()


def create_message_from_file(file_path: str):
    with open(file_path, "r") as f:
        html_code = f.read()
    return '\n'.join([
        "HTTP/1.1 200 OK",
        "Content-Type: text/html",
        f"Content-Length: {len(html_code)}",
        "",
        html_code
    ])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(1)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            request = conn.recv(1024).decode('utf-8')
            if request:
                response = create_message_from_file("static/index.html")
                conn.sendall(response.encode("utf-8"))
```