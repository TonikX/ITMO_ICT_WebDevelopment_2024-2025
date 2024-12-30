import socket

HOST = '127.0.0.1'
PORT = 16000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect((HOST, PORT))
print(f'Client sent: Hello server')

client.sendall(b'Hello server')
data, _ = client.recvfrom(1024)

print(f'Client received: {data.decode()}')