import socket

# Создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к IP и порту
server_socket.bind(('localhost', 8080))

print("Сервер запущен на порту 8080...")

while True:
    # Принимаем сообщение от клиента
    message, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от {client_address}: {message.decode()}")

    # Отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
