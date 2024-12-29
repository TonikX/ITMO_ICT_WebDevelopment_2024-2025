import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostname(), 1234))

while True:
    data, address = s.recvfrom(1024)
    udata = data.decode('utf-8')
    print(f'Data received: {udata}')
    s.sendto(b'Hello, client!', address)
