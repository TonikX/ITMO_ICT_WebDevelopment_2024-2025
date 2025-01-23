import socket


def start_client():
    server_address = ("127.0.0.1", 12345)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)
        print("Подключение к серверу установлено.")
        print("Введите коэффициенты квадратного уравнения или 'exit' для завершения.")

        while True:
            message = input("Введите a, b, c через пробел: ")
            if message.strip().lower() == "exit":
                client_socket.sendall(message.encode())
                print("Завершение работы клиента.")
                break

            client_socket.sendall(message.encode())

            result = client_socket.recv(1024).decode()
            print(f"Результат от сервера: {result}")


if __name__ == "__main__":
    start_client()
