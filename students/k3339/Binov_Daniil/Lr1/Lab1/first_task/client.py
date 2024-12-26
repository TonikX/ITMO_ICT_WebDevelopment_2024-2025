import socket

server_port = 12345
buffer_size = 1024

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', server_port)

    message = 'Hello, server'
    client_socket.sendto(message.encode(), server_address)

    response, _ = client_socket.recvfrom(buffer_size)
    print(f'Получено сообщение: {response.decode()}')


if __name__ == '__main__':
    udp_client()