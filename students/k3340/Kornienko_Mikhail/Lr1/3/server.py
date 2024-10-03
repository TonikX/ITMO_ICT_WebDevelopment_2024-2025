import socket


headers = """HTTP/1.1 200 OK
            Content-Type: text/html\n\n"""
file = open(file='index.html').read()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(("127.0.0.1", 3000))

serv.listen(5)

while True:
    sock, _ = serv.accept()
    sock.recv(1024)
    sock.sendall(headers.encode())
    sock.sendall(file.encode())
