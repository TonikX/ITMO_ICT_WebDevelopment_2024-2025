import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 12345))
s.listen(1)

while True:
    conn, addr = s.accept()

    data = conn.recv(1024).decode('utf-8')
    a, b = data.split()
    a = int(a)
    b = int(b)
    pif = (a**2+b**2)**0.5

    conn.send(str(pif).encode())
    conn.close()

s.close()