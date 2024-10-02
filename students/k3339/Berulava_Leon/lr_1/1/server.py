import socket

# Создание UDP-сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязка сокета к IP и порту
server_address = ('127.0.0.1', 65432)
server_socket.bind(server_address)

print("UDP сервер запущен и ожидает сообщений...")

while True:
    # Ожидание сообщения от клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f"Получено сообщение от {client_address}: {data.decode()}")

    # Ответ клиенту (опционально)
    response = "Hello client"
    server_socket.sendto(response.encode(), client_address)
