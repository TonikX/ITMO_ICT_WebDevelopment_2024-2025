import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

a = int(input("Введите длину основания a: "))
b = int(input("Введите длину основания b: "))
h = int(input("Введите высоту h: "))

message = f"{a} {b} {h}"
client_socket.send(message.encode())

result = client_socket.recv(1024).decode()
print(f"Площадь параллелограмма: {result}")

client_socket.close()