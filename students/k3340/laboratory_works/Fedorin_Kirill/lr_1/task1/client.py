import socket


def start_client() -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)

    # Отправляем сообщение серверу
    message = 'Hello, server'
    client_socket.sendto(message.encode(), server_address)
    print('Сообщение отправлено серверу')

    # Получаем ответ от сервера
    response, _ = client_socket.recvfrom(1024)
    print(f'Ответ от сервера: {response.decode()}')

    client_socket.close()


if __name__ == '__main__':
    start_client()
