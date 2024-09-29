import socket


def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 12123)
    server_socket.bind(server_address)

    print("Server is running...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"Received a message: {data.decode('utf-8')}")

        server_socket.sendto(b"Hello, client", client_address)


if __name__ == "__main__":
    udp_server()
