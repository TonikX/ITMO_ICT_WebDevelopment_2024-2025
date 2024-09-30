import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

a = input("Введите длину первого катета: ")
b = input("Введите длину второго катета: ")

client_socket.send(f"{a},{b}".encode())

data = client_socket.recv(1024).decode()
print(f"Гипотенуза: {data}")

client_socket.close()