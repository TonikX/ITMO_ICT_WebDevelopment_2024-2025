import socket


def run_server(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''Запуск простого HTTP-сервера'''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(1)
        print(f'HTTP-сервер слушает на {server_host}:{server_port}')
        conn, _ = server.accept()

        with conn:
            conn.recv(1024)
            with open('index.html', 'r', encoding='utf-8') as f:
                body = f.read()

            response = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/html; charset=utf-8\r\n'
                f'Content-Length: {len(body.encode())}\r\n'
                '\r\n'
                f'{body}'
            )
            conn.sendall(response.encode())


if __name__ == '__main__':
    run_server()
