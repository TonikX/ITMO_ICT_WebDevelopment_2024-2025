import socket


def start_tcp_client(host='127.0.0.1', port=8000):
    request = "Hello server, please send index.html file".encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(request)

        data = client_socket.recv(1024)
        print(f'Received from server: {data.decode("utf-8")}')


if __name__ == "__main__":
    start_tcp_client()
