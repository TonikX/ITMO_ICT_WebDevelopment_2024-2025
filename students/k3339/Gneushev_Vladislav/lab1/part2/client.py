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
