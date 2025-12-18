import socket


def run_client(server_host: str = '127.0.0.1', server_port: int = 8081):
    '''Запуск UDP-клиента'''

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.sendto('Hello, server'.encode(), (server_host, server_port))
        data, _ = client.recvfrom(1024)
        print(f'Ответ от сервера: {data.decode()}')


if __name__ == '__main__':
    run_client()
