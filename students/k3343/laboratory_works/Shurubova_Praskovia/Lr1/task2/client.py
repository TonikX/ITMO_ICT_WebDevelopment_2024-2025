import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

response = client_socket.recv(1024).decode()
a = input("Сторона, к которой проведена высота: ")
h = input("Высота: ")
client_socket.send(f"{a} {h}".encode())
result = client_socket.recv(1024)
print(f'Ответ от сервера: {result.decode()}')

client_socket.close()