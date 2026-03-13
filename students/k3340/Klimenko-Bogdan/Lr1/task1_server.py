import socket

# Настройки сервера
SERVER_HOST = '127.0.0.1'   
SERVER_PORT = 12345          # порт для приёма сообщений
BUFFER_SIZE = 1024           # размер буфера для приёма данных

# 1. Создаём UDP-сокет (SOCK_DGRAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Привязываем сокет к адресу и порту
server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"UDP-сервер запущен на {SERVER_HOST}:{SERVER_PORT} и ожидает сообщения...")

try:
    while True:
        # 3. Получаем данные от клиента
        # recvfrom возвращает кортеж: (данные, адрес_клиента)
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        message = data.decode('utf-8')
        print(f"Получено сообщение от {client_address}: {message}")

        # 4. Отправляем ответ
        response = "Hello, client"
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлен ответ клиенту {client_address}: {response}")

except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()