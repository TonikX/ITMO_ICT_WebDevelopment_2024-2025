import socket
import math

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024


def calculate(request):
    try:
        operation, *args = request.split(',')
        args = list(map(float, args))

        if operation == "1":  # Теорема Пифагора
            a, b = args
            result = math.sqrt(a ** 2 + b ** 2)
            return f"Гипотенуза: {result:.2f}"

        elif operation == "2":  # Решение квадратного уравнения
            a, b, c = args
            discriminant = b ** 2 - 4 * a * c
            if discriminant > 0:
                x1 = (-b + math.sqrt(discriminant)) / (2 * a)
                x2 = (-b - math.sqrt(discriminant)) / (2 * a)
                return f"Корни уравнения: x1={x1:.2f}, x2={x2:.2f}"
            elif discriminant == 0:
                x = -b / (2 * a)
                return f"Единственный корень: x={x:.2f}"
            else:
                return "Нет действительных корней"

        elif operation == "3":  # Площадь трапеции
            a, b, h = args
            result = ((a + b) / 2) * h
            return f"Площадь трапеции: {result:.2f}"

        elif operation == "4":  # Площадь параллелограмма
            base, height = args
            result = base * height
            return f"Площадь параллелограмма: {result:.2f}"

        else:
            return "Неизвестная операция"
    except (ValueError, IndexError):
        return "Ошибка обработки данных. Проверьте ввод."


def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Подключение от клиента: {addr}")
            with conn:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    request = data.decode()
                    print(f"Получено сообщение: {request}")

                    response = calculate(request)
                    conn.sendall(response.encode())


if __name__ == "__main__":
    tcp_server()
