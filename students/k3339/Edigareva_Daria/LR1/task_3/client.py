import socket


def fetch_html():
    HOST = '127.0.0.1'
    PORT = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    request = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"

    client_socket.sendall(request.encode())

    response = client_socket.recv(4096).decode()

    print("Полученный ответ от сервера:")
    print(response)

    client_socket.close()


if __name__ == "__main__":
    fetch_html()
