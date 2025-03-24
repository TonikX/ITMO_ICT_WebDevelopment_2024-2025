import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем сообщение от клиента
    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    # Высчитываем площадь параллелограмма
    a, h = str(request).split(' ')
    response = str(int(a) * int(h))

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())

    # Закрываем соединение
    client_connection.close()
