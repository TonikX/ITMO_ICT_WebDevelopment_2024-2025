import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('localhost', 8080)

client.sendto(b"Hello, server", address)
data, server = client.recvfrom(1024)
print(data.decode('utf-8'))
client.close()