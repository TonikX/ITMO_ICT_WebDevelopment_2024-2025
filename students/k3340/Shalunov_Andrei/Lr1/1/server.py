import socket

IP = 'localhost'
PORT = 8080

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((IP, PORT))

response, client_address = server_sock.recvfrom(1024)
print(response.decode())

message = 'Hello, client'
server_sock.sendto(message.encode(), client_address)
server_sock.close()