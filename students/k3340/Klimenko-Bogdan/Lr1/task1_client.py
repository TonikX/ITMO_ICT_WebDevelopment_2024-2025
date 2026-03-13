import socket

# Настройки сервера, к которому подключаемся
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# 1. Создаём UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
print(f"Отправлено серверу: {message}")

# 3. Получаем ответ от сервера
# recvfrom также возвращает данные и адрес, но адрес нам не обязателен
data, server_address = client_socket.recvfrom(BUFFER_SIZE)
response = data.decode('utf-8')
print(f"Получен ответ от сервера: {response}")

# 4. Закрываем сокет
client_socket.close()