import socket

HOST = "127.0.0.1"
PORT = 50001

a = float(input("Введите первый катет: "))
b = float(input("Введите второй катет: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(f"{a} {b}".encode())

data = client.recv(1024).decode()
print(f"Гипотенуза: {data}")

client.close()
