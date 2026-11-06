import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode(), ("127.0.0.1", 12345))

data, address = client.recvfrom(1024)
print(data.decode())

client.close()