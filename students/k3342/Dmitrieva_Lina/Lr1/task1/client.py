import socket

server_address = ('localhost', 8080)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    message = 'Hello, server'
    print(f'Отправка сообщения серверу: {message}')
    sent = server_socket.sendto(message.encode(), server_address)

    message, server = server_socket.recvfrom(1024)
    print(f'Получено сообщение от сервера: {message.decode()}')

finally:
    server_socket.close()
