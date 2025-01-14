import socket

IP = "127.0.0.1"
PORT = 4000
BUFFER = 1024
HEADERS = """HTTP/1.1 200 OK
            Content-Type: text/html\n\n"""
DATA = open(file='index.html').read()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))

print("Server started!")

serv.listen(1)

while True:
    sock, _ = serv.accept()
    sock.recv(BUFFER)
    sock.sendall(HEADERS.encode())
    sock.sendall(DATA.encode())
