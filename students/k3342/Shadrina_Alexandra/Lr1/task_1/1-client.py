import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8080)

client_socket.sendto(b'Hello, server', server_address)

response, server = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
