import socket


def start_server():
    # Создаем UDP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)

    print("Сервер запущен и ожидает сообщения...")

    while True:
        # Принимаем сообщение от клиента
        message, client_address = server_socket.recvfrom(1024)
        print(f"Получено сообщение от клиента: {message.decode()}")

        # Отправляем ответ клиенту
        response = "Hello, client"
        server_socket.sendto(response.encode(), client_address)
        print(f"Отправлено сообщение клиенту: {response}")


if __name__ == "__main__":
    start_server()
