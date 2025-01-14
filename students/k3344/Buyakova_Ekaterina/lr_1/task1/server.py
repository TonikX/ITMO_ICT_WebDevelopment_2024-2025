import socket

# Создаем сокет с использованием UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

print("Server starts on port 8080...")

while True:
    # Получаем сообщение от клиента и адрес клиента
    message, client_address = server_socket.recvfrom(1024)
    print(f'Message from client: {message.decode()}')

    # Отправляем ответ клиенту
    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
