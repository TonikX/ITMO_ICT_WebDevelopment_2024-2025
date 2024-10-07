import socket

# Создаем UDP-сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
message = "Hello, server"
sock.sendto(message.encode(), ('localhost', 12345))

# Получаем ответ от сервера
data, server = sock.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

sock.close()