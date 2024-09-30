import socket
import math

port = 12345
buffer_size = 1024
max_connections = 1

def math_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(max_connections)
    print("Сервер запущен. Ожидание подключения...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")

        data = client_socket.recv(buffer_size).decode('utf-8')
        a, b = map(float, data.split(','))

        c = math.sqrt(a ** 2 + b ** 2)
        print(f"Вычисление: a={a}, b={b}, c={c}")

        client_socket.sendall(str(c).encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    math_server()