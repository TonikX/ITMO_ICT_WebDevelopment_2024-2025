import socket

HOST = 'localhost'
PORT = 8081
BUFFER_SIZE = 1024

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #dgram тк udp
    client_socket.sendto("Hello, server!".encode(), (HOST, PORT))

    data, server = client_socket.recvfrom(BUFFER_SIZE)
    print(f"Server response: {data.decode()}")


if __name__ == "__main__":
    main()

