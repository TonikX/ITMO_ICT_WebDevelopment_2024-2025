import socket

HOST = "127.0.0.1"
PORT = 5001

a = input("Введите a: ")
b = input("Введите b: ")
c = input("Введите c: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f"{a} {b} {c}".encode("utf-8"))
    data = s.recv(1024).decode("utf-8")

print("Ответ от сервера:", data)
