import socket

# Создаем UDP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Сообщение для отправки серверу
server_message = "Hello, server"

# Отправляем сообщение серверу
client_socket.sendto(server_message.encode(), ('localhost', 8080))

# Получаем ответ от сервера
response, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode()}")

# Закрываем сокет
client_socket.close()
