import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

a = input("Введите длину стороны a: ")
b = input("Введите длину стороны b: ")

client_socket.sendall(f"{a} {b}".encode())

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()