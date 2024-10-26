import socket
import math

# Параметры сервера
HOST = 'localhost'
PORT = 8080

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие соединения
server_socket.listen(5)
print(f"Сервер запущен на {HOST}:{PORT}...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем данные от клиента
    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    # Парсим параметры для теоремы Пифагора (a и b)
    try:
        a, b = map(float, request.split())
        # Вычисляем гипотенузу
        c = math.sqrt(a ** 2 + b ** 2)
        response = f'Гипотенуза равна: {c:.2f}'
    except Exception as e:
        response = f'Ошибка: {str(e)}'

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())

    # Закрываем соединение
    client_connection.close()
