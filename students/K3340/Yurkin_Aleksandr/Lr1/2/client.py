import socket

IP = "127.0.0.1"
PORT = 4000
BUFFER = 1024

print("Pythagoras calc")
a = input("A = ")
b = input("B = ")

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((IP, PORT))
serv.sendall(f'{a} {b}'.encode())
data = serv.recv(BUFFER)

print("Calculated C =", data.decode())
