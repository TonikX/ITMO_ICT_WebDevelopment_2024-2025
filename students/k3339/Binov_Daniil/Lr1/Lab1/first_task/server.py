import socket

port = 12345
buffer_size = 1024

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', port)
    server_socket.bind(server_address)

    print('Сервер запущен, ожидает сообщения...')

    while True:
        data, client_address = server_socket.recvfrom(buffer_size)
        print(f'Получено сообщение: {data.decode()} от {client_address}')

        response = 'Hello, client'
        server_socket.sendto(response.encode(), client_address)

if __name__ == '__main__':
    udp_server()