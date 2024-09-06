from socket import socket, AF_INET, SOCK_DGRAM


def udp_client(server_address: tuple[str, int] = ('localhost', 12345)):
    """
    Функция создает UDP клиента на заданном сокете для
    отправки серверу сообщения 'Hello, server' и печати
    полученного ответа
    :param server_address: Тупл с указанием ip адреса и порта для сокета.
    ('localhost', 12345) по умолчанию
    :type server_address:  tuple[str, int]
    :return: None
    :rtype: None
    """
    client_socket = socket(AF_INET, SOCK_DGRAM)

    try:
        message = b"Hello server\n"
        print(f"Sending: {message}")
        client_socket.sendto(message, server_address)

        response, _ = client_socket.recvfrom(1024)
        print(f"Received: {response.decode()}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    udp_client()
