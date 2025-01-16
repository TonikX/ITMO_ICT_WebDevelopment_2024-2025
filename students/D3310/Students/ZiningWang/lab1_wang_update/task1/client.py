from socket import *


client_socket = socket(AF_INET, SOCK_DGRAM)

data_for_server = "Hello, Server!"

client_socket.sendto(data_for_server.encode(), ('localhost', 9090))
print(f"Message: '{data_for_server}' was sent to server.")

data_from_server, addr = client_socket.recvfrom(1024)
print(f"Message: '{data_from_server.decode()}' was received from server.")
