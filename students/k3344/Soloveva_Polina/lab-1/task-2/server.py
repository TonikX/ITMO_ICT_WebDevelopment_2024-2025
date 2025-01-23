import socket
import math


def solve_quadratic(a, b, c):
    """Решение квадратного уравнения ax^2 + bx + c = 0"""
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Два корня: {root1}, {root2}"
    elif discriminant == 0:
        root = -b / (2 * a)
        return f"Один корень: {root}"
    else:
        return "Корней нет"


def start_server():
    server_address = ("127.0.0.1", 12345)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen(1)
        print("Сервер запущен и ожидает подключений...")

        while True:
            connection, client_address = server_socket.accept()
            with connection:
                print(f"Подключен клиент: {client_address}")
                while True:
                    data = connection.recv(1024).decode()
                    if not data or data.strip().lower() == "exit":
                        print("Клиент завершил соединение.")
                        break

                    try:
                        a, b, c = map(float, data.split())
                        result = solve_quadratic(a, b, c)
                    except ValueError:
                        result = "Ошибка: некорректные данные. Введите три числа."

                    connection.sendall(result.encode())


if __name__ == "__main__":
    start_server()
