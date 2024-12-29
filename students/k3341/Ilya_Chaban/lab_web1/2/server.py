import math
import socket
# TCP


def quadraticEquation(a, b, c):
    D = (b * b - 4 * a * c)
    if D == 0:
        x = (-b + math.sqrt(D)) / (2 * a)
        return x
    elif D > 0:
        x1 = (-b - math.sqrt(D)) / (2 * a)
        x2 = (-b + math.sqrt(D)) / (2 * a)
        return x1, x2
    else:
        return "No solution"


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", 7070))
serverSocket.listen(1)

while True:
    client_socket, client_address = serverSocket.accept()

    data = client_socket.recv(1024).decode()
    a, b, c = map(float, data.split())

    ans = quadraticEquation(a, b, c)

    client_socket.send(str(ans).encode())

    client_socket.close()
