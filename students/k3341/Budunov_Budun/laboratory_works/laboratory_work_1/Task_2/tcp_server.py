import socket
import math


def solve_quadratic(a, b, c):
    # Решение квадратного уравнения ax^2 + bx + c = 0
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Два корня: x1 = {root1}, x2 = {root2}"
    elif discriminant == 0:
        root = -b / (2 * a)
        return f"Один корень: x = {root}"
    else:
        return "Корней нет (дискриминант отрицательный)"


def start_server():
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)

    # Ожидаем подключения клиентов
    server_socket.listen(1)
    print("Сервер запущен и ожидает подключения...")

    while True:
        # Принимаем соединение от клиента
        connection, client_address = server_socket.accept()
        try:
            print(f"Подключение от клиента: {client_address}")

            # Получаем данные от клиента
            data = connection.recv(1024).decode()
            if data:
                # Преобразуем строку данных в параметры a, b и c
                a, b, c = map(float, data.split(','))
                print(f"Получено уравнение с параметрами: a={a}, b={b}, c={c}")

                # Решаем квадратное уравнение
                result = solve_quadratic(a, b, c)

                # Отправляем результат клиенту
                connection.sendall(result.encode())
                print(f"Результат отправлен клиенту: {result}")
        finally:
            # Закрываем соединение
            connection.close()


if __name__ == "__main__":
    start_server()
