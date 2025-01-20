import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Получаем локальный IP-адрес и порт
server_address = ('localhost', 7777)

server_socket.bind(server_address)

while True:
    print('Ожидание сообщения...')
    data, address = server_socket.recvfrom(4096)

    print(data.decode())

    if data:
        sent = server_socket.sendto(b'Hello, client', address)