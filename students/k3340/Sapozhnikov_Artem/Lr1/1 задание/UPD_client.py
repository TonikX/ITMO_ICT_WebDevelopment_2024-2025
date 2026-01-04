import socket

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
client_socket.sendto(b"Hello, server!", ('localhost', 9090))

# Ждем ответ от сервера
data, server = client_socket.recvfrom(1024)
print(f"Answer from server: {data.decode()}")

client_socket.close()
