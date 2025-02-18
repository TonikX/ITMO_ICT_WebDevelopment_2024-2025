import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8081))
server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    eq_params = request.split(" ")
    a = int(eq_params[0])
    b = int(eq_params[1])
    c = int(eq_params[2])
    discr = b ** 2 - 4 * a * c
    if discr > 0:
        x1 = (-b + math.sqrt(discr)) / (2 * a)
        x2 = (-b - math.sqrt(discr)) / (2 * a)
        response = "x1 = %.2f \nx2 = %.2f" % (x1, x2)
        client_connection.sendall(response.encode())

    elif discr == 0:
        x = -b / (2 * a)
        response = "x = %.2f" % x
        client_connection.sendall(response.encode())

    else:
        response = "Корней нет"
        client_connection.sendall(response.encode())

    client_connection.close()

