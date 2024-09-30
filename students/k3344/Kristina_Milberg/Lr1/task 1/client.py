import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8080)

# Отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Сообщение отправлено серверу: {message}")

# Получаем ответ от сервера
response, _ = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode('utf-8')}")

client_socket.close()