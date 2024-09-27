import socket

IP = 'localhost'
PORT = 8080
message = 'Hello, server'

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.sendto(message.encode(), (IP, PORT))

response, server_address = client_sock.recvfrom(1024)
print(response.decode())
client_sock.close()