import socket

IP = 'localhost'
PORT = 8080


def findSquare(a, h):
    return a * h

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((IP, PORT))
server_sock.listen()

while True:
    connection, address = server_sock.accept()
    print(connection, address)
    data = connection.recv(1024).decode()
    a, h = map(float, data.split(','))
    connection.sendall(str(findSquare(a, h)).encode())
    connection.close()
