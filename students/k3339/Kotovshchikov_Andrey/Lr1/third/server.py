import pathlib
import socket

HOST = "127.0.0.1"
PORT = 8000
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024
BASE_DIR = pathlib.Path("third")


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    while True:
        client, _ = server.accept()
        client.recv(BUFFER_SIZE)
        client.send(b"HTTP/1.1 200 OK\n")
        client.send(b"Content-Type: text/html\n")
        client.send(b"\n")
        client.send((BASE_DIR / "index.html").read_bytes())

    server.close()


if __name__ == "__main__":
    serve()
