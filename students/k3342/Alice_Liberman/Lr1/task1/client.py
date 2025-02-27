from socket import socket, AF_INET, SOCK_DGRAM


def task_1():
    _Host = 'localhost'
    _port = 55555

    client = socket(AF_INET, SOCK_DGRAM)
    client.sendto(b'Hello, Server!', (_Host, _port))

    message, server_port = client.recvfrom(2024)
    print(f'Server on {server_port} has said: {message.decode()}')

    client.close()


if __name__ == '__main__':
    task_1()
