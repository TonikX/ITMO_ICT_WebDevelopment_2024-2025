import math
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime


def solve_quadratic(a: float, b: float, c: float) -> str:  # ищет корни квадратного уравнения

    discriminant = b ** 2 - 4 * a * c

    if discriminant >= 0:
        x_1 = (-b + math.sqrt(discriminant)) / 2 * a
        x_2 = (-b - math.sqrt(discriminant)) / 2 * a
    else:
        x_1 = complex((-b / (2 * a)), math.sqrt(-discriminant) / (2 * a))
        x_2 = complex((-b / (2 * a)), -math.sqrt(-discriminant) / (2 * a))

    if discriminant > 0:
        return f"Уравнение имеет два корня: {x_1} и  {x_2}"
    elif discriminant == 0:
        return f"У уравнения два повторяющихся корня: {x_1}"
    else:
        return f"Уравнение не имеет решений"


def validate_data(data: str) -> list[float]:  # проверяет введеные пользователем данные, при некорректном вводе возращает пустой список

    data = data.strip().replace(',', '.').split()
    if len(data) != 3 or not \
            all(digint.replace('.', '').isdigit() for digint in data):
        return []
    return list(map(float, data))


def solver_server(socket_address: tuple[str, int] = ('localhost', 12345)) -> None:  # создает сервер на заданном порту, возвращает решение уравнения

    server = socket(AF_INET, SOCK_STREAM)
    server.bind(socket_address)

    server.listen(5)

    print(f'Started listening on {socket_address}')

    while True:
        try:
            client_socket, client_address = server.accept()
            print(f'Connected from {client_address}')
            message = client_socket.recv(1024).decode('utf-8')
            print(f'Received message from client: {message}\nValidating data...')
            params = validate_data(message)  # irrelevant helper function
            if params:
                solution = solve_quadratic(*params)
                print(f'The data is valid\nsending back to client at {datetime.now().time()}: \n{solution}')
                client_socket.send(solution.encode('utf-8'))
            else:
                # if params are wrong
                print('The data is invalid')
                client_socket.send('Некорректный ввод'.encode('utf-8'))
        except KeyboardInterrupt:
            print('shutting down')
            server.close()
            return


if __name__ == '__main__':
    solver_server()