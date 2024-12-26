import socket


def area(a, b, h):
    return (a + b) / 2 * h


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(("127.0.0.1", 2000))

print("Server started!")

serv.listen()

while True:
    sock, _ = serv.accept()
    data = sock.recv(1024).decode()
    a, b, h = data.split(',')
    sock.sendall(str(area(float(a), float(b), float(h))).encode())
