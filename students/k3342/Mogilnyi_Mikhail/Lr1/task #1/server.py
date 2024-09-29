import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

while True:
    data, addr = server.recvfrom(BUFFER_SIZE)
    print(data.decode())
    server.sendto(b'HELLO FROM SERVER', addr)
