from socket import socket, AF_INET, SOCK_DGRAM


def task_1():
    _Host = 'localhost'
    _port = 55555

    server = socket(AF_INET, SOCK_DGRAM)
    server.bind((_Host, _port))

    print(f'Server listening for udp requests on {_Host}:{_port}')

    message, client_port = server.recvfrom(2024)
    print(f'Client on {client_port} has said: {message.decode()}')

    server.sendto(b'Hello, client!', client_port)

    server.close()


if __name__ == '__main__':
    task_1()
