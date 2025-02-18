import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = 'Hello, server'

client_socket.sendto(message.encode(), ('localhost', 8081))

response, _ = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
