from socket import socket, AF_INET, SOCK_DGRAM


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.bind(("localhost", 8080))

    while True:
        data, addr = sock.recvfrom(1024)
        print(data.decode())

        sock.sendto(b"Hello, client", addr)
