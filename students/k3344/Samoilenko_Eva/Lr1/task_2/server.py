import socket
import math

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
serv_sock.bind(serv_address)
serv_sock.listen(1)

print('connected:', serv_address)

while True:
    conn, cl_address = serv_sock.accept()
    try:
        data = conn.recv(1024).decode()
        a, b = map(float, data.split())
        if a <= 0 or b <= 0:
            conn.send('the sides cannot be negative or equal zero'.encode())
        hypotenuse = math.sqrt(a**2 + b**2)
        conn.send(f'length of hypotenuse = {hypotenuse}'.encode())
    finally:
        conn.close()
