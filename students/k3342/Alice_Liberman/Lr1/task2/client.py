from socket import socket, AF_INET, SOCK_STREAM


def tcp_client(server_address: tuple[str, int] = ('localhost', 12345)) -> None:

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(server_address)

    data = input("Введите коэффициенты a, b, c для квадратного уравнения: ")
    client_socket.send(data.encode('UTF-8'))
    print(client_socket.recv(1024).decode('UTF-8'))
    client_socket.close()


if __name__ == "__main__":
    tcp_client()