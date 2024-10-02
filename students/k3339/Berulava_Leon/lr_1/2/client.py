import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

print("Введи два числа")
chislo = input()

client_socket.send(chislo.encode())

result = client_socket.recv(1024).decode()

print("Гипотенуза =", result)

client_socket.close()