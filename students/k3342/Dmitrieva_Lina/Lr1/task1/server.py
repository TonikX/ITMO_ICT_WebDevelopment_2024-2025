import socket

server_address = ('localhost', 8080)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(server_address)
print('Сервер запущен на порте и ждет сообщений')

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f'Получено сообщение от клиента: {message.decode()}')

    if message:
        response = 'Hello, client!'
        server_socket.sendto(response.encode(), client_address)
        print(f'Отправлено сообщение клиенту: {response}')