import socket

# Настройка клиента
SERVER_IP = '127.0.0.1'  # IP-адрес сервера
SERVER_PORT = 12345       # Порт сервера
CLIENT_PORT = 54321

# Создание сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1', CLIENT_PORT))

# Отправка сообщения серверу
message = "Hello, server"
client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# Получение ответа от сервера
response, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode()}")