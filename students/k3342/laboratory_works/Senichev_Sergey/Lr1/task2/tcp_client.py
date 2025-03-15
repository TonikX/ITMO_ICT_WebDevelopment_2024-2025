import socket

port = 8080
host = 'localhost'
server_address = (host, port)

a = input("Enter first base (a): ")
b = input("Enter second base (b): ")
h = input("Enter height (h): ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

client_socket.sendall(f"{a} {b} {h}".encode())

result = client_socket.recv(1024).decode()
print(f"{result}")

client_socket.close()