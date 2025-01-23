import socket


def start_server():
    server_address = ("127.0.0.1", 12345)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(server_address)
        print("Сервер запущен и ожидает сообщений...")

        while True:
            data, client_address = server_socket.recvfrom(1024)
            print(f"Сообщение от клиента {client_address}: {data.decode()}")

            response = "Hello, client"
            server_socket.sendto(response.encode(), client_address)


if __name__ == "__main__":
    start_server()
