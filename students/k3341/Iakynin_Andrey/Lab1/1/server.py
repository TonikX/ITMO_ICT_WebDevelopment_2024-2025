import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.bind(('', 6061))


while True:
    data, addr = sock.recvfrom(1024)
    print(data.decode())
    if not data:
        break

    sock.sendto("Hello, client".encode(), addr)


sock.close()
