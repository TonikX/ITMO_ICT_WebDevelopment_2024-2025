import socket

IP = "127.0.0.1"
PORT = 4000
BUFFER = 1024

print("Расчет площади трапеции")
a = input("Введите основание a: ")
b = input("Введите основание b: ")
h = input("Введите высоту h: ")

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((IP, PORT))
serv.sendall(f'{a} {b} {h}'.encode())
data = serv.recv(BUFFER)

print("Площадь трапеции =", data.decode())
