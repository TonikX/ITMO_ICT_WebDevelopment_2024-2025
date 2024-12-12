import socket

response = 'Hello, client'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8080))

while True:
    request, client_address = server_socket.recvfrom(1024)

    print(request.decode())

    server_socket.sendto(response.encode(), client_address)
