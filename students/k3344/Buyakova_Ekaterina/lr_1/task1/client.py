import socket

# Создаем сокет с использованием UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
server_address = ('localhost', 8080)
client_socket.sendto(b'Hello, server', server_address)

# Получаем ответ от сервера
response, _ = client_socket.recvfrom(1024)
print(f'Server response: {response.decode()}')

# Закрываем сокет
client_socket.close()
