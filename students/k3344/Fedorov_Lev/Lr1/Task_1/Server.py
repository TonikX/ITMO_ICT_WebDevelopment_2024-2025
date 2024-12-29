import socket

HOST = 'localhost'
PORT = 8081
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print("Server is online")

    while True:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        decoded_data = data.decode()

        print(f"Message from client: {decoded_data}")

        server_socket.sendto("Hello, client!".encode(), client_address)


if __name__ == "__main__":
    main()
