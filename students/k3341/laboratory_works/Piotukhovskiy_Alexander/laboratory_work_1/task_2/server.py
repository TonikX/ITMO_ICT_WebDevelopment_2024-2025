import json
import socket

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024
MAX_CONNECTIONS = 10


def calculate_area_trapezoid(a, b, h):
    return (a + b) * h / 2


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_CONNECTIONS)
print("Server is running")

while True:
    client, _ = server.accept()
    data = client.recv(BUFFER_SIZE)
    if data == "stop_server":
        break
    j = json.loads(data)
    a, b, h = j["a"], j["b"], j["h"]
    area_trapezoid = calculate_area_trapezoid(a, b, h)
    client.send(f"{area_trapezoid}".encode())
server.close()
