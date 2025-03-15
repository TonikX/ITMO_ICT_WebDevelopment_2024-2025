import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'HELLO FROM CLIENT', (HOST, PORT))

data, addr = client.recvfrom(BUFFER_SIZE)
print(data.decode())