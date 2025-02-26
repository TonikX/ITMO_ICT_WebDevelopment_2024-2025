import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 1234)

message = 'Hello server'
client.sendto(message.encode(), server_address)

data, server = client.recvfrom(1024)
print(f'Ответ от сервера: {data.decode()}')

client.close()
