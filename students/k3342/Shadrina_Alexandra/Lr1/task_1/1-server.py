import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))
print("Сервер запущен на порту 8080...")

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f'Получено сообщение от {client_address}: {message.decode()}')

    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
