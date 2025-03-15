import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("Hello, server".encode(), ("localhost", 1234))

server_message, server_address = client_socket.recvfrom(1024)
print("Recieved message:", server_message.decode())
