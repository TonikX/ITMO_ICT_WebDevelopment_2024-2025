import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('localhost', 8080)

client_socket.sendto('Hello, server!'.encode(), address)

data, server_address = client_socket.recvfrom(1024)
print('Message from server: ', data.decode())

client_socket.close()

