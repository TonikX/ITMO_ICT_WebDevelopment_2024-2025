from socket import socket, AF_INET, SOCK_DGRAM


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.sendto(b"Hello, server", ("localhost", 8080))

    data, server = sock.recvfrom(1024)
    print(f"{data.decode()}")
