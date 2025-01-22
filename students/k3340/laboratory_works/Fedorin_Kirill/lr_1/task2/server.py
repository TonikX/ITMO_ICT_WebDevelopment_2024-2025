import math
import socket


def solve_quadratic(a: float, b: float, c: float) -> str:
    # Вычисление дискриминанта
    discriminant = b**2 - 4 * a * c
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f'Два корня: x1 = {root1}, x2 = {root2}'
    if discriminant == 0:
        root = -b / (2 * a)
        return f'Один корень: x = {root}'
    return 'Нет действительных корней'


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print('TCP сервер запущен и ожидает подключения...')

    while True:
        conn, addr = server_socket.accept()
        print(f'Клиент подключен: {addr}')

        data = conn.recv(1024).decode()
        if data:
            # Преобразуем входные данные в коэффициенты
            try:
                a, b, c = map(float, data.split(','))
                result = solve_quadratic(a, b, c)
            except ValueError:
                result = 'Некорректные данные. Пожалуйста, введите три числа, разделенные запятой.'

            conn.send(result.encode())  # Отправляем результат клиенту
            print(f'Результат отправлен клиенту {addr}')

        conn.close()


if __name__ == '__main__':
    start_server()
