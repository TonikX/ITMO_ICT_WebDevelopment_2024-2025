import socket
import math


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)
    print("Сервер запущен и ожидает запросов...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        if message.decode('utf-8') == "gimme index.html":
            with open("index.html") as f:
                server_socket.sendto(str(f.read()).encode('utf-8'), client_address)


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 8080)

    client_socket.sendto("gimme index.html".encode('utf-8'), server_address)

    reply, _ = client_socket.recvfrom(1024)
    print(reply.decode('utf-8'))

    client_socket.close()


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()
    else:
        print("Некорректный выбор. Пожалуйста, выберите 'server' или 'client'.")
