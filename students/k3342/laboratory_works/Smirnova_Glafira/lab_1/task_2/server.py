import socket
import math


def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        a, b = map(float, data.split())

        if a <= 0 or b <= 0:
            raise Exception
        c = math.sqrt(a ** 2 + b ** 2)

        client_socket.sendall(f"Гипотенуза: {c:.2f}".encode())
    except Exception as e:
        client_socket.sendall(f"Ошибка: {str(e)}".encode())
    finally:
        client_socket.close()


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Подключен клиент: {addr}")
        handle_client(client_socket)


if __name__ == "__main__":
    start_server('127.0.0.1', 65432)
