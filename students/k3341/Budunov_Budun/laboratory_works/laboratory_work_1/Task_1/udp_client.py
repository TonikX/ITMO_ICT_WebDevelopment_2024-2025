import socket


def start_client():
    # Создаем UDP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Адрес сервера
    server_address = ('localhost', 8080)

    # Отправляем сообщение серверу
    message = "Hello, server"
    client_socket.sendto(message.encode(), server_address)
    print(f"Отправлено сообщение серверу: {message}")

    # Получаем ответ от сервера
    response, _ = client_socket.recvfrom(1024)
    print(f"Получено сообщение от сервера: {response.decode()}")

    # Закрываем сокет
    client_socket.close()


if __name__ == "__main__":
    start_client()
