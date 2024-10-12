import socket

IP = "127.0.0.1"
PORT = 4000
BUFFER = 1024

def pythagoras(a, b):
    return (a**2 + b**2)**0.5


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))

print("Server started!")

serv.listen()

while True:
    sock, _ = serv.accept()
    data = sock.recv(BUFFER).decode()
    a, b = data.split()
    sock.sendall(str(pythagoras(float(a), float(b))).encode())
