import socket
import json

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024


a, b, h = map(
    lambda x: float(x.strip()),
    input("Введите длины двух оснований трапеции и высоту. \nРазделяйте значения запятой.\n").strip().split(","),
)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(json.dumps(dict(a=a, b=b, h=h)).encode())

response = client.recv(BUFFER_SIZE)
area = float(response.decode())

print(f"Площадь = {area}")
client.close()
