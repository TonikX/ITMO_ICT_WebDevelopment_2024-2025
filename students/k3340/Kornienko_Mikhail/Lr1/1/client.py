import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.sendto("Hello, server".encode(), ("127.0.0.1", 1000))

data, addr = serv.recvfrom(1024)
print("Message:", data.decode())
