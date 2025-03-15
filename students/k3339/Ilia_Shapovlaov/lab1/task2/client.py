from socket import socket, AF_INET, SOCK_STREAM


with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect(("localhost", 8080))
    client_socket.sendall(
        input(
            "Введите длины двух смежных сторон и высоту через пробел "
        ).encode()
    )
    data = client_socket.recv(1024)
    print("Ответ сервера: ", data.decode("utf-8"))
