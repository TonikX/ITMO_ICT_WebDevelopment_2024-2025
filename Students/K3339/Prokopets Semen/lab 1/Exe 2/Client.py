import socket


def start_client(host='localhost', port=777):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        a = input("Введите длину первого катета: ")
        b = input("Введите длину второго катета: ")
        client_socket.sendall(f"{a} {b}".encode())

        data = client_socket.recv(1024)
        print(f"Гипотенуза: {data.decode()}")
    finally:
        client_socket.close()


# Запуск клиента
start_client()