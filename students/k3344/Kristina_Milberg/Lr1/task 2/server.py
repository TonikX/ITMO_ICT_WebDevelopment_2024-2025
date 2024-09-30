import socket


def calculate_trapezoid_area(a, b, h):
    """Функция для вычисления площади трапеции."""
    return (a + b) * h / 2


server_address = ('localhost', 8080)

# Создание TCP-сокета
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
sock.bind(server_address)

# Ожидаем подключения клиента
sock.listen(1)
print('Сервер запущен и ожидает подключения клиента...')

while True:
    # Принятие соединения
    connection, client_address = sock.accept()
    try:
        print(f'Подключен клиент: {client_address}')

        # Получаем данные от клиента
        data = connection.recv(1024).decode()
        print(f'Получены данные: {data}')

        if data:
            # Разбираем данные (длины оснований и высота)
            a, b, h = map(float, data.split(','))

            # Вычисляем площадь трапеции
            area = calculate_trapezoid_area(a, b, h)

            # Отправляем результат обратно клиенту
            connection.sendall(str(area).encode())
            print(f'Результат отправлен клиенту: {area}')
    finally:
        connection.close()