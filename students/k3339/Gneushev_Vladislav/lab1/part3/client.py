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
