from datetime import datetime  # for logging
from socket import socket, AF_INET, SOCK_DGRAM


def udp_server(server_address: tuple[str, int] = ('localhost', 12345)) -> None:
    """
    Функция создает UDP сервер на заданном сокете для
    печати сообщения от клиента и отправки ему текста 'Hello, client!'.
    :param server_address: Тупл с указанием ip адреса и порта для сокета.
    ('localhost', 12345) по умолчанию
    :type server_address: tuple[str, int]
    :return: None
    :rtype: None
    """
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(server_address)
    # set up the socket

    print(f"Server is up and listening on {server_address}")

    while True:
        try:
            # main loop
            message, client_address = server_socket.recvfrom(1024)
            print(f"Received message from {client_address} at {datetime.now().time()}: {message.decode()}")

            response = b"Hello client!\n"
            server_socket.sendto(response, client_address)
        except KeyboardInterrupt:
            server_socket.close()
            break


if __name__ == "__main__":
    udp_server()
