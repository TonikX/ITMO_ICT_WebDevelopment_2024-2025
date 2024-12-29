import socket
a = float(input())
b = float(input())
c = float(input())

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 7070))

client_socket.send(f"{a} {b} {c}".encode())


data = client_socket.recv(1024).decode()
print(data)

client_socket.close()