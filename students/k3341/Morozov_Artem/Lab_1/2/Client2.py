import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

a = float(input("Введите коэффициент a: "))
b = float(input("Введите коэффициент b: "))
c = float(input("Введите коэффициент c: "))
params = str(a) + " " + str(b) + " " + str(c)

client_socket.sendall(params.encode())

data = client_socket.recv(1024).decode()
print(f"Ответ сервера: {data}")

client_socket.close()