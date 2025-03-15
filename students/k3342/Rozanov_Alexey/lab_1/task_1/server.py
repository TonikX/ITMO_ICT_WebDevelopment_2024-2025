import socket
import signal


def raise_timeout(signum, frame):
    """
    Функция для рейза ошибки таймаута
    :param signum:
    :param frame:
    :return:
    """
    raise TimeoutError


if __name__ == '__main__':

    signal.signal(signal.SIGALRM, raise_timeout)

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', 8088)
    socket_server.bind(server_address)

    signal.alarm(60)  # убиваем таймаутом после минуты ожидания

    try:
        while True:
            data, address = socket_server.recvfrom(1024)
            print(f"Client with ip {address[0]} and port {address[1]} sent a message: {data.decode()}")

            response = "Hello, client"
            socket_server.sendto(response.encode(), address)
            break
    finally:
        signal.alarm(0)
