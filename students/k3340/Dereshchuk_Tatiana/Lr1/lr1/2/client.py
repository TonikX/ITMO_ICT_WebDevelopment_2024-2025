import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

a = int(input("Введите длину первого катета: "))
b = int(input("Введите длину второго катета: "))

message = f"{a} {b}"
client_socket.send(message.encode())

result = client_socket.recv(1024).decode()
print(f"Результат вычисления теоремы Пифагора: {result}")

client_socket.close()