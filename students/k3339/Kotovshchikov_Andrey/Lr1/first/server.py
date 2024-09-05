import socket

PORT = 8000
HOST = socket.gethostname()
MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))

    while True:
        request_data, client_address = server.recvfrom(BUFFER_SIZE)
        decoded_data = request_data.decode()
        print(decoded_data)
        server.sendto("Hello client".encode(), client_address)

    server.close()


if __name__ == "__main__":
    serve()
