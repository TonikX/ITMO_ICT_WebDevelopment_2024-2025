import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((socket.gethostname(), 1234))
s.send(b"Hello, server \n")

while True:
    msg = s.recv(1024)
    umsg = msg.decode('utf-8')
    print(f'Data received: {umsg}')

