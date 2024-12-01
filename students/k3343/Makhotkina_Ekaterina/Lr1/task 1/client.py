import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)
message = 'Hello, server!'
client_socket.sendto(message.encode(), server_address)
response, _ = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()
