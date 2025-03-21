import socket
import json

host = socket.gethostname()
port = 8000


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(7)

    print(f'http://{host}:{port}')

    while True:
        client, _ = server.accept()
        request_data = client.recv(1024)
        variables = json.loads(request_data)
        square = variables['side'] * variables['height']
        client.send(f"{square}".encode())
        client.close()


if __name__ == "__main__":
    server()