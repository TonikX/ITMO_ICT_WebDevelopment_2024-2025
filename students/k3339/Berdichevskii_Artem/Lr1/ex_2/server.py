import math
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 65432))
sock.listen()
conn, addr = sock.accept()

with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        a, b = map(float, data.split())
        c = math.sqrt(a ** 2 + b ** 2)
        conn.sendall(f"{c}".encode('utf-8'))