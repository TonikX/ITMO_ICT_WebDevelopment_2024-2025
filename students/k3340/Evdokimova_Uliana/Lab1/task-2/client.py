import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

a = float(input("Введите коэффициент a: "))
b = float(input("Введите коэффициент b: "))
c = float(input("Введите коэффициент c: "))

message = f"{a} {b} {c}"
client_socket.send(message.encode())

result = client_socket.recv(1024).decode()
print(f"Решение уравнения: {result}")

client_socket.close()
