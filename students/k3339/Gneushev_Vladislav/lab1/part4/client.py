import socket
import threading
from contextlib import contextmanager

from server.constants import SERVER_HOST, SERVER_PORT


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


def handle_message(sock):
    while True:
        data = sock.recv(1024)
        print(data.decode("utf-8"))


def main():
    with client() as c:
        threading.Thread(target=handle_message, args=(c,)).start()
        while True:
            message = input()
            send_message(c, message)


if __name__ == "__main__":
    main()
