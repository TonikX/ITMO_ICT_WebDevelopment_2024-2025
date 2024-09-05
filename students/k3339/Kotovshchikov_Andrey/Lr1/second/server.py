import math
import socket
import json

HOST = socket.gethostname()
PORT = 8000
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


def calculate_hypotenuse(a: float, b: float) -> float:
    return math.sqrt(a**2 + b**2)


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    while True:
        client, _ = server.accept()
        request_data = client.recv(BUFFER_SIZE)
        cathets = dict(json.loads(request_data))
        hypotenuse = calculate_hypotenuse(**cathets)
        client.send(f"{hypotenuse}".encode())

    server.close()


if __name__ == "__main__":
    serve()
