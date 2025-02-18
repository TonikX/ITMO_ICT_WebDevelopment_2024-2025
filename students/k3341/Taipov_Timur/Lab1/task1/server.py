import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8081))

while True:

    data, client_address = server_socket.recvfrom(1024)

    if data.decode() == "Hello, server":
        response = 'Hello, client'
        server_socket.sendto(response.encode(), client_address)

    else:
        response = "Bye"
        server_socket.sendto(response.encode(), client_address)
