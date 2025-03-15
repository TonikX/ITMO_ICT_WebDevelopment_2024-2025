import socket
import math

def solve_quadratic(a, b, c):
    """Решение квадратного уравнения."""
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        # Два действительных корня
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Два корня: x1 = {x1}, x2 = {x2}"
    elif discriminant == 0:
        # Один действительный корень
        x = -b / (2 * a)
        return f"Один корень: x = {x}"
    else:
        # Действительных корней нет
        return "Корней нет (дискриминант отрицательный)"

server_address = ('localhost', 8080)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(server_address)

sock.listen(1)
print('Сервер запущен и ожидает подключения клиента...')

while True:
    connection, client_address = sock.accept()
    try:
        print(f'Подключен клиент: {client_address}')

        data = connection.recv(1024).decode()
        print(f'Получены данные: {data}')

        if data:
            a, b, c = map(float, data.split(','))
            
            result = solve_quadratic(a, b, c)
            
            connection.sendall(result.encode())
            print(f'Результат отправлен клиенту: {result}')
    finally:
        connection.close()
