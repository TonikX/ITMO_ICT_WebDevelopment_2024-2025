from socket import socket, AF_INET, SOCK_STREAM


def tcp_client(server_address: tuple[str, int] = ('localhost', 12345)):
    """
    Функция создает TCP клиента на заданном сокете, для
    того чтобы принять от пользователя параметры квадратичного
    уравнения, отправить их на сервер и вернуть ответ
    :param server_address: Tuple с указанием ip адреса и порта для сокета.
    ('localhost', 12345) по умолчанию
    :type server_address:  tuple[str, int]
    :return: None
    :rtype: None
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(server_address)

    data = input("give me the 'a b c' of a quadratic equation for me to solve: ")
    client_socket.send(data.encode('UTF-8'))
    print(client_socket.recv(1024).decode('UTF-8'))
    client_socket.close()


if __name__ == "__main__":
    tcp_client()
