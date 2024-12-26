import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


client_socket.sendto(b'Hello, server', ('localhost', 8080))

response, server_address = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()