import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, server"

client_socket.sendto(message.encode('utf-8'), ('localhost', 12345))

response, server = client_socket.recvfrom(1024)
print(f"{response.decode('utf-8')}")

client_socket.close()
