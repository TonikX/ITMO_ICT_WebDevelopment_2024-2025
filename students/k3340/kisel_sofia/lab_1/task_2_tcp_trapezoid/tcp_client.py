import socket


def run_client(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''Запуск TCP-клиента'''

    a = input('Введите основание a: ')
    b = input('Введите основание b: ')
    h = input('Введите высоту h: ')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_host, server_port))
        client.sendall(f'{a},{b},{h}'.encode())
        data = client.recv(1024)
        print(f'Площадь трапеции: {data.decode()}')


if __name__ == '__main__':
    run_client()
