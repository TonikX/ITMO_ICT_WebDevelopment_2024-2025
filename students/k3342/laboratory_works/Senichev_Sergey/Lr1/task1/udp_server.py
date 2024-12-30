import socket

buffer_size = 1024
port = 8080
host = 'localhost'
server_address = (host, port)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    print(f"UDP server has started on {host}:{port}")

    while True:
        message, client_address = server_socket.recvfrom(buffer_size)
        print(f"Client message: {message.decode()}")
        server_socket.sendto(b"Hello client", client_address)

    server_socket.close()

if __name__ == "__main__":
    server()
