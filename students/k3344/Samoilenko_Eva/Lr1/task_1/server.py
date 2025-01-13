import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_address = ('localhost', 8080)
sock.bind(serv_address)

print('connected:', serv_address)

while True:
    data, cl_address = sock.recvfrom(1024)
    print(data.decode())
    sock.sendto('hello, client!'.encode(), cl_address)
