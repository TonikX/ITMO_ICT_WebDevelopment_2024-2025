import math
import socket


def solve_quadratic_equation(a, b, c):
    d = b ** 2 - 4 * a * c

    if d > 0:
        return (-b + math.sqrt(d)) / 2 * a, (-b - math.sqrt(d)) / 2 * a
    elif d == 0:
        return -b / 2 * a
    else:
        return 'Решений нет'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', 8080))

    server_socket.listen(1)
    client_connection, client_address = server_socket.accept()

    with client_connection:
        print(f'Подключение от {client_address}')

        data = client_connection.recv(1024).decode()
        print(f'Запрос от клиента: {data}')

        a_str, b_str, c_str = data.split()
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)

        result = str(solve_quadratic_equation(a, b, c))

        client_connection.sendall(result.encode())
