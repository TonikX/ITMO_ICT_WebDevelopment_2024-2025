import socket
import math


def solve_quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        ans = [x1, x2]
    elif discriminant == 0:
        x = -b / (2 * a)
        ans = [x]
    else:
        ans = []
    return " ".join(list(map(str, ans)))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode()

    try:
        a1, b1, c1 = map(float, request.split())
        result = solve_quadratic(a1, b1, c1)
    except ValueError:
        result = "Error: Введите три действительных числа."

    client_socket.sendall(result.encode())
    client_socket.close()
