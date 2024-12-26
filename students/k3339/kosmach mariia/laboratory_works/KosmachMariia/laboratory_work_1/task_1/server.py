import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', 14900))

data, client_address = server.recvfrom(16384)
print(data.decode("UTF-8"))

server.sendto(b"Hello, client", client_address)
server.close()