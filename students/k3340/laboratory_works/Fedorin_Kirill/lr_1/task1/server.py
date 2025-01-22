import socket


def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12345))
    print('UDP сервер запущен и ожидает сообщения...')

    while True:
        message, client_address = server_socket.recvfrom(1024)  # Получаем сообщение от клиента
        print(f'Сообщение от клиента {client_address}: {message.decode()}')

        # Отправляем ответ клиенту
        response = 'Hello, client'
        server_socket.sendto(response.encode(), client_address)
        print(f'Ответ отправлен клиенту {client_address}')


if __name__ == '__main__':
    start_server()
