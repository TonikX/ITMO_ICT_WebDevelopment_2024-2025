import socket
import math


def handle_client(client_socket):
    # Получаем данные от клиента
    data = client_socket.recv(1024).decode()
    try:
        a, b = map(float, data.split(","))
        c = math.sqrt(a ** 2 + b ** 2)
        result = f"Гипотенуза: {c:.2f}"
    except Exception as e:
        result = f"Ошибка обработки данных: {str(e)}"

    client_socket.send(result.encode())
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 65432))
    server_socket.listen(5)
    print("Сервер запущен и ожидает соединений...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключён клиент: {addr}")
        handle_client(client_socket)


if __name__ == "__main__":
    main()