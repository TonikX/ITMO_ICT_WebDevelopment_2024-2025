import socket
import math


def start_server(host='localhost', port=777):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Сервер запущен, ожидаем подключения...")

    try:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Подключено к {addr}")
            data = conn.recv(1024).decode()
            if data:
                a, b = map(float, data.split())
                hypotenuse = math.sqrt(a ** 2 + b ** 2)
                conn.sendall(str(hypotenuse).encode())
    finally:
        server_socket.close()


# Запуск сервера
start_server()