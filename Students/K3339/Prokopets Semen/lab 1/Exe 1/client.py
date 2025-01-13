import socket
# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Получаем локальный IP-адрес и порт
server_address = ('localhost', 7777)

message = 'Hello, server'.encode()

try:
    # Отправляем данные
    sent = client_socket.sendto(message, server_address)

    data, server = client_socket.recvfrom(4096)

    print(data.decode())

finally:
    print('Закрытие сокета')
    client_socket.close()