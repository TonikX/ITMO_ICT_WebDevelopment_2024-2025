import socket

IP = "127.0.0.1"
PORT = 4000
BUFFER = 1024

def trapezoid_area(a, b, h):
    return ((a + b) * h) / 2

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))

print("Сервер запущен!")

serv.listen()

while True:
    sock, _ = serv.accept()
    data = sock.recv(BUFFER).decode()
    a, b, h = data.split()
    area = trapezoid_area(float(a), float(b), float(h))
    sock.sendall(str(area).encode())
