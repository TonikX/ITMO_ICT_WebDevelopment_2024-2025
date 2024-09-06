from socket import socket, AF_INET, SOCK_STREAM


def encode_args(*args):
    return (''.join(args) + '\n\n').encode('utf-8')


def html_server(socket_address: tuple[str, int] = ('localhost', 12345)):
    """
    Создает простой html сервер с 1 статичной разметкой из ./index.html
    :param socket_address: Tuple с указанием ip адреса и порта для сокета.
    ('localhost', 12345) по умолчанию
    :type socket_address: tuple[str, int]
    :return: None
    :rtype: None
    """
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(socket_address)
    server.listen(5)

    print(f'Started listening on {socket_address}')
    print(f'to see the result, go to http://{socket_address[0]}:{socket_address[1]}')

    standard_headers = [
        'HTTP/1.1 200 OK\r\n',
        'Content-Type: text/html; charset=utf-8\r\n',
        '\r\n'
    ]

    while True:
        try:
            with open('index.html', 'r') as f:
                html = f.read()
            client_socket, client_address = server.accept()
            print(f'Connected from {client_address}')
            client_socket.recv(1024)
            client_socket.send(encode_args(*standard_headers, *html))
        except KeyboardInterrupt:
            print('shutting down')
            server.close()
            return


if __name__ == '__main__':
    html_server()
