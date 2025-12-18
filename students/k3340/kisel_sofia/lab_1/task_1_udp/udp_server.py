import socket


def run_server(server_host: str = '127.0.0.1', server_port: int = 8081):
    '''Запуск UDP-сервера'''

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((server_host, server_port))
        print(f'UDP-сервер слушает на {server_host}:{server_port}')

        data, addr = server.recvfrom(1024)
        if data:
            print(f'Сообщение от клиента {addr}: {data.decode()}')
            server.sendto('Hello, client'.encode(), addr)


if __name__ == '__main__':
    run_server()
