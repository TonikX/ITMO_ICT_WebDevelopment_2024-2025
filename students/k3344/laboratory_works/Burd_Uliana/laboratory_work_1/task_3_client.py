import socket

HOST = 'localhost'
PORT = 5005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n')
    data = s.recv(1024)
    if data:
        html = data.split(b'\r\n\r\n')[1].decode('utf-8')
        print(html)
