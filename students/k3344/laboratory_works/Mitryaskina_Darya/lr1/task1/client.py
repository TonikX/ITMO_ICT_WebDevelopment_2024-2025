import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.connect((socket.gethostname(), 1234))
conn.send(b"Hello, server.\n")
msg = conn.recv(1024)
umsg = msg.decode('utf-8')
print(umsg)