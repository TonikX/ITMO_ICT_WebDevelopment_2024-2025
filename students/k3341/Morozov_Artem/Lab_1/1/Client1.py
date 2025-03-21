import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес и хост
client_socket.connect(('localhost', 8080))

client_socket.sendall(b'Hello, server')

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()