import socket


def calculate_trapezoid_area(a: float, b: float, h: float) -> float:
    '''
    Подсчёт площади трапеции по формуле
    S = (a + b) * h / 2
    '''
    return (a + b) * h / 2


def run_server(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''Запуск TCP-сервера'''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(1)
        print(f'Сервер слушает на {server_host}:{server_port}')
        conn, addr = server.accept()

        with conn:
            print(f'Подключено клиентом {addr}')
            data = conn.recv(1024)

            if data:
                a, b, h = map(float, data.decode().split(','))
                result = calculate_trapezoid_area(a, b, h)
                conn.sendall(str(result).encode())


if __name__ == '__main__':
    run_server()
