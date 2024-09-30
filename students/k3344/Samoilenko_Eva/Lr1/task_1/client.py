import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_address = ('localhost', 8080)

sock.sendto('hello, server!'.encode(), serv_address)

data, _ = sock.recvfrom(1024)
print(data.decode())
sock.close()
