from socket import *

client_socket = socket(AF_INET, SOCK_DGRAM)

data_for_server = "Hello, server!"

client_socket.sendto(data_for_server.encode(), ('localhost', 12345))
print(f"Message: '{data_for_server}' was sent to server.")

data_from_server, addr = client_socket.recvfrom(1024)
print(f"Message: '{data_from_server.decode()}' was received from server.")


