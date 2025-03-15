import socket


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54001)
    server_socket.bind(server_address)
    print("Сервер запущен и ожидает сообщений...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Сообщение от клиента: {message.decode('utf-8')}")

        reply = "Hello, client"
        server_socket.sendto(reply.encode('utf-8'), client_address)


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 54001)

    message = "Hello, server"
    client_socket.sendto(message.encode('utf-8'), server_address)

    reply, _ = client_socket.recvfrom(1024)
    print(f"Ответ от сервера: {reply.decode('utf-8')}")

    client_socket.close()


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()
    else:
        print("Некорректный выбор. Пожалуйста, выберите 'server' или 'client'.")
