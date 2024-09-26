import socket


content = open("index.html").read()

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(("127.0.0.1", 8081))
conn.listen()

while True:
    socket = conn.accept()[0]
    data = socket.recv(1024)
    response = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" + content
    socket.send(response.encode())
    socket.close()