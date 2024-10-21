import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 1936)
server.bind(server_address)

while True:
    data, client_address = server.recvfrom(1024)
    print("Message from client:", data.decode())
    response = "Hello, client"
    server.sendto(response.encode(), client_address)