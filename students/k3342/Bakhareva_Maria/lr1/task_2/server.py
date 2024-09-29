import socket
import math

def solve_quadratic(a, b, c):
    D = b ** 2 - 4 * a * c
    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        return f"Два решения: x1 = {x1}, x2 = {x2}"
    elif D == 0:
        x = -b / (2 * a)
        return f"Одно решение: x = {x}"
    else:
        return "Нет действительных решений"

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Сервер запущен и ожидает подключения...")

try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Подключено к {addr}")

        try:
            data = conn.recv(1024).decode()
            a, b, c = map(float, data.split())
            result = solve_quadratic(a, b, c)
            conn.send(result.encode())
        except Exception as e:
            conn.send(f"Ошибка: {str(e)}".encode())
        finally:
            conn.close()
except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()
