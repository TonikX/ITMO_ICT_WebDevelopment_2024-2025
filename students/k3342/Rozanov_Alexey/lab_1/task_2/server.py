import socket
import math
import signal


def raise_timeout(signum, frame):
    """
    Функция для рейза ошибки таймаута
    :param signum:
    :param frame:
    :return:
    """
    raise TimeoutError


def handle_client(socket_user):
    """
    Client handler. Gets data from client
    and counts hippotenuse
    :param socket_user:
    :return:
    """
    user_data = socket_user.recv(1024).decode('utf-8')
    if not user_data:
        raise ValueError('The data is empty')

    try:
        a, b, alpha = map(float, user_data.split())
        result = round(a * b * math.sin(math.radians(alpha)), 2)
        socket_user.send(f"Square: {result}".encode('utf-8'))
    except ValueError:
        socket_user.send("Error: incorrect data".encode('utf-8'))
    finally:
        socket_user.close()


def start_server():
    """
    starting the server, waiting for client
    and using handle_client()
    :return:
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8088))
    server.listen(5)
    print("Server is up and ready")

    while True:
        socket_user, addr = server.accept()
        print(f"Client {addr} is connected")
        handle_client(socket_user)


if __name__ == "__main__":

    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(60)

    try:
        start_server()
    finally:
        signal.alarm(0)
