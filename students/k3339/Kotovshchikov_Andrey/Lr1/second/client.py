import socket
import json

SERVER_HOST = socket.gethostname()
SERVER_PORT = 8000
BUFFER_SIZE = 1024

a, b = map(
    lambda cathet: float(cathet.strip()),
    input("Катеты прямоугольного треугольника ").strip().split(","),
)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))
client.send(json.dumps(dict(a=a, b=b)).encode())

response_data = client.recv(BUFFER_SIZE)
hypotenuse = float(response_data.decode())

print(f"Гипотенуза = {hypotenuse}")
client.close()
