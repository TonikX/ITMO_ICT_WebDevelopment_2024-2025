import socket


def start_udp_server():
    serv_address = ('localhost', 8080)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(serv_address)
        print('Сервер запущен и подключен по адресу:', serv_address)

        while True:
            data, cl_address = sock.recvfrom(1024)
            print('Получено сообщение от клиента:', data.decode())
            response = 'Hello, client!'
            sock.sendto(response.encode(), cl_address)
            print('Отправлено сообщение клиенту:', response)


if __name__ == "__main__":
    start_udp_server()
