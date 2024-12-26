import socket

server_address = ('localhost', 14900)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello, server", server_address)

data = client.recv(16384)
print(data.decode("UTF-8"))

client.close()