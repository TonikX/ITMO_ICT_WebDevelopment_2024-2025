import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = b'Hello, Server!'
client_sock.sendto(message, ('localhost', 8080))

data, addr = client_sock.recvfrom(1024)
print(f'ответ от сервера: {data.decode("utf-8")}')

client_sock.close()