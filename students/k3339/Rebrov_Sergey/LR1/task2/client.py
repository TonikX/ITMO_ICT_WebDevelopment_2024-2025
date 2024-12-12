import socket

a, b, c = 1, 2, -3

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

client_socket.send(f"{a} {b} {c}".encode())
result = client_socket.recv(1024)

print(list(map(float, result.decode().split())))

client_socket.close()
