import socket

# Создание UDP-сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес сервера
server_address = ('127.0.0.1', 65432)

# Отправка сообщения серверу
message = "hello server"
client_socket.sendto(message.encode(), server_address)

# Получение ответа от сервера (опционально)
data, server = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

# Закрытие сокета
client_socket.close()

