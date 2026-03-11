import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12346))

a = input("Введите катет a: ")
b = input("Введите катет b: ")

client.send(f"{a} {b}".encode())

result = client.recv(1024).decode()
print("Гипотенуза =", result)

client.close()
