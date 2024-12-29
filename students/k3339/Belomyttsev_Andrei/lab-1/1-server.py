import socket

IP = '127.0.0.1'
PORT = 2020

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP, PORT))
data, address = server.recvfrom(1024)
print(data.decode('utf-8'))
server.sendto(b'Hello, client\n', address)
server.close()