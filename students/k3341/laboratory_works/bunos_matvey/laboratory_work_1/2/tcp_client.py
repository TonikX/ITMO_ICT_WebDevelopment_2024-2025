import socket

HOST = '127.0.0.1'
PORT = 65432

a = input("Enter side a: ")
b = input("Enter side b: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f"{a},{b}".encode())
    data = s.recv(1024)

print(f"The length of the hypotenuse is {data.decode()}")
