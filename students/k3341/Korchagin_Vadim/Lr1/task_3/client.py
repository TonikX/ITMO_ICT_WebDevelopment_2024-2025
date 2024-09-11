import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1234))

msg = s.recv(1024)
umsg = msg.decode('utf-8')
print(umsg)
s.close()
