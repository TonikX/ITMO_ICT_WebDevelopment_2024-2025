import socket

# Настройки сервера
SERVER_IP = 'localhost' 
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Разрешить повторное использование адреса
server_socket.bind(('localhost', 8080))

# Слушаем входящие подключения
server_socket.listen(1)
print(f"Сервер запущен на {SERVER_IP}:{SERVER_PORT} и ожидает подключений...")

while True:
    # Принимаем соединение от клиента
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент с адресом {client_address}")

    try:
        # Получаем сообщение с параметрами (основание и высота)
        data = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Получены данные от клиента: {data}")

        # Разбиваем параметры и вычисляем площадь параллелограмма
        base, height = map(float, data.split(","))
        area = base * height
        print(f"Вычисленная площадь параллелограмма: {area}")

        # Отправляем результат обратно клиенту
        client_socket.send(str(area).encode())
    except Exception as e:
        print(f"Ошибка: {e}")
        client_socket.send(f"Ошибка обработки данных: {e}".encode())

    # Закрываем соединение с клиентом
    client_socket.close() 