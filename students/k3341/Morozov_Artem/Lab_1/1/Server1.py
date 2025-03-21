import socket

def server():
    server_address = ('localhost', 8080)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Адрес и хост
    sock.bind(server_address)

    print("Сервер запущен.")

    while True:
        data, client_address = sock.recvfrom(4096)
        print(f"Получено сообщение от клиента: {data.decode()}")

        message = "Hello, client"
        sock.sendto(message.encode(), client_address)
        print(f"Отправлено сообщение клиенту: {message}")


if __name__ == "__main__":
    server()