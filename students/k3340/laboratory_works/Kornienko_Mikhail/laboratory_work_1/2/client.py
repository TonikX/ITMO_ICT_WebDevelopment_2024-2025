import socket

print("Area of trapezoid")
a = input("A = ")
b = input("B = ")
h = input("H = ")

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect(("127.0.0.1", 2000))
serv.sendall(f'{a},{b},{h}'.encode())
data = serv.recv(1024)

print("Calculated S = ", data.decode())
