import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.bind(("127.0.0.1", 1000))

while True:
    data, addr = serv.recvfrom(1024)
    print("Message:", data.decode())
    serv.sendto("Hello, client".encode(), addr)
