import socket

IP = '127.0.0.1'
PORT = 2020

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'Hello, server\n', (IP, PORT))
data, address = client.recvfrom(1024)
print(data.decode('utf-8'))
client.close()