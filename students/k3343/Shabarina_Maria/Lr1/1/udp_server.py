import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 1234))

print("Server started")

client_message, client_address = server_socket.recvfrom(1024)
print("Recieved message:", client_message.decode())
server_socket.sendto("Hello, client".encode(), client_address)
