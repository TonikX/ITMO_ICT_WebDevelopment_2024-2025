import socket


def start_client():
    server_address = ("127.0.0.1", 12345)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        message = "Hello, server"
        client_socket.sendto(message.encode(), server_address)
        print(f"Сообщение отправлено серверу: {message}")

        data, _ = client_socket.recvfrom(1024)
        print(f"Ответ от сервера: {data.decode()}")


if __name__ == "__main__":
    start_client()
