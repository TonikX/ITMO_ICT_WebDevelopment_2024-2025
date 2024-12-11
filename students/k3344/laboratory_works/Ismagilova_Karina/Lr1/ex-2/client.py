import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

a = input("Длина первого катета: ")
b = input("Длина второго катета: ")

client_socket.send(f"{a} {b}".encode())

response = client_socket.recv(1024)
print(f'Ответ: {response.decode()}')

client_socket.close()
