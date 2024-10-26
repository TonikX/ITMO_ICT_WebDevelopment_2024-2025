import socket

# Параметры сервера
HOST = 'localhost'  # Адрес сервера
PORT = 8080         # Порт сервера

# Создаем сокет для UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Сообщение для отправки серверу
message = "Hello, server"
client_socket.sendto(message.encode(), (HOST, PORT))

# Получаем ответ от сервера
response, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode()}")

# Закрываем сокет
client_socket.close()