import socket

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8080))

print("Сервер ожидает сообщение...")

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от клиента: {message.decode()}")

    # Ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
