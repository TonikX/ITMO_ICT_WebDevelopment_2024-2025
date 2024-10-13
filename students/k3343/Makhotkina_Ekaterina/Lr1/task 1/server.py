import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)
server_socket.bind(server_address)

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f'{message.decode()}')
    response = 'Hello client!'
    server_socket.sendto(response.encode(), client_address)