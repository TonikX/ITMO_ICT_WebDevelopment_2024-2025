import socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('localhost',14901))
a = float(input("Введите длину первого основания (a): "))
b = float(input("Введите длину второго основания (b): "))
h = float(input("Введите высоту (h): "))
client_sock.send(f"{a} {b} {h}".encode())
data = client_sock.recv(1024).decode()
print(data)
client_sock.close()
