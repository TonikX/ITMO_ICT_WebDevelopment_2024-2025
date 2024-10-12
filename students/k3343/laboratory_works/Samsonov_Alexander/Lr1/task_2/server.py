import math
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime


def solve_quadratic(a: float, b: float, c: float) -> str:
    """
    Функция считает корни квадратного уравнения и возвращает
    строку с ними. Поддерживает также комплексные ответы.
    На вход принимает параметры в данной последовательности:
    a * X^2 + b * X + c
    :param a: первый параметр квадратичного уравнения
    :param b: второй параметр квадратичного уравнения
    :param c: третий параметр квадратичного уравнения
    :return: строка с ответом на квадратичное уравнения
    :rtype: str
    """
    discriminant = b ** 2 - 4 * a * c

    if discriminant >= 0:
        x_1 = (-b + math.sqrt(discriminant)) / 2 * a
        x_2 = (-b - math.sqrt(discriminant)) / 2 * a
    else:
        x_1 = complex((-b / (2 * a)), math.sqrt(-discriminant) / (2 * a))
        x_2 = complex((-b / (2 * a)), -math.sqrt(-discriminant) / (2 * a))

    if discriminant > 0:
        return f"The function has two distinct real roots: {x_1} and  {x_2}"
    elif discriminant == 0:
        return f"The function has one double root: {x_1}"
    else:
        return f"The function has two complex (conjugate) roots: {x_1} and {x_2}"


def validate_data(data: str) -> list[float]:
    """
    Функция для валидации поступивших данных. Входная строка
    должна содержать 3 числа через пробел. При невозможности распарсить -
    возвращает пустой список
    :param data: строка от клиента, должна быть формата: num1 num2.2 num 3,3
    :type data: str
    :return: либо пустой, либо список с распарсенными цифрами
    :rtype: list[float]
    """
    data = data.strip().replace(',', '.').split()
    if len(data) != 3 or not \
            all(digint.replace('.', '').isdigit() for digint in data):
        return []
    return list(map(float, data))


def solver_server(socket_address: tuple[str, int] = ('localhost', 12345)) -> None:
    """
    Функция создает TCP сервер на заданом порту. Он принимает сообщения из
    3 цифр и возвращает решение квадратного уравнения
    :param socket_address: Tuple с указанием ip адреса и порта для сокета.
    ('localhost', 12345) по умолчанию
    :type socket_address: tuple[str, int]
    :return: None
    :rtype: None
    """
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(socket_address)

    server.listen(5)
    # socket setup

    print(f'Started listening on {socket_address}')

    while True:
        # main loop
        try:
            client_socket, client_address = server.accept()
            print(f'Connected from {client_address}')
            message = client_socket.recv(1024).decode('utf-8')
            print(f'Received message from client: {message}\nValidating data...')
            params = validate_data(message)  # irrelevant helper function
            if params:
                solution = solve_quadratic(*params)  # irrelevant helper function
                print(f'The data is valid\nsending back to client at {datetime.now().time}: \n{solution}')
                client_socket.send(solution.encode('utf-8'))
            else:
                # if params are wrong
                print('The data is invalid')
                client_socket.send('Invalid parameters, try again.'.encode('utf-8'))
        except KeyboardInterrupt:
            print('shutting down')
            server.close()
            return


if __name__ == '__main__':
    solver_server()
