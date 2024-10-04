from socket import socket, AF_INET, SOCK_DGRAM

def client(_Host, _port):

    client = socket(AF_INET, SOCK_DGRAM)
    client.sendto(b'Hello, server', (_Host, _port))

    response, _ = client.recvfrom(2024)
    print(f'Message from server: {response.decode()}')

    client.close()


if __name__ == '__main__':
    task1_client('localhost', 2024)