import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 9090))
print("UDP-server was launched on port 9090...")

while True:
    # Получаем сообщение от клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f"Message from client {client_address}: {data.decode()}")

    # Отправляем ответ клиенту
    response = "Hello, client!"
    server_socket.sendto(response.encode(), client_address)
