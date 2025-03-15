import socket
import math


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54002)
    server_socket.bind(server_address)
    print("Сервер запущен и ожидает запросов...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        a, b = map(float, message.decode('utf-8').split(','))
        print(f"Получены катеты: a={a}, b={b}")

        c = math.sqrt(a ** 2 + b ** 2)
        print(f"Вычисленная гипотенуза: c={c}")

        server_socket.sendto(str(c).encode('utf-8'), client_address)


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54002)

    a = float(input("Введите длину первого катета: "))
    b = float(input("Введите длину второго катета: "))

    message = f"{a},{b}"
    client_socket.sendto(message.encode('utf-8'), server_address)

    reply, _ = client_socket.recvfrom(1024)
    print(f"Результат (гипотенуза): {reply.decode('utf-8')}")

    client_socket.close()


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()
    else:
        print("Некорректный выбор. Пожалуйста, выберите 'server' или 'client'.")
