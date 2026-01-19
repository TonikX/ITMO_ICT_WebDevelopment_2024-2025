from socket import socket, AF_INET, SOCK_DGRAM

# Создаем UDP-сокет
# используем AF_INET, чтобы работать с IP-адресами (IPv4), и SOCK_DGRAM для использования протокола UDP
client_socket = socket(AF_INET, SOCK_DGRAM)

# Адрес сервера
server_address = ('localhost', 8080)

# Отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Отправлено сообщение: {message}")

# Получаем ответ от сервера
data, server = client_socket.recvfrom(1024)
response = data.decode('utf-8')
print(f"Получен ответ от сервера: {response}")

# Закрываем сокет
client_socket.close()
