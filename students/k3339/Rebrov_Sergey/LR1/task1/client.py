import socket

request = 'Hello, server'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(('localhost', 8080))

client_socket.send(request.encode())
response, server_address = client_socket.recvfrom(1024)

print(response.decode())

client_socket.close()
