import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Сервер запущен")

def hypotenuse_calc(a, b):
    return math.sqrt(a**2 + b**2)

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    triangle = client_connection.recv(1024).decode()
    a, b = map(float, triangle.split())
    hypotenuse = hypotenuse_calc(a, b)
    response = f"Гипотенуза: {hypotenuse:.2f}"

    client_connection.send(response.encode())
    # client_connection.close()
