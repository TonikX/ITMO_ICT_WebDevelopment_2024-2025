import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

client_socket.sendall(f'Hello, server'.encode('utf-8'))

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()