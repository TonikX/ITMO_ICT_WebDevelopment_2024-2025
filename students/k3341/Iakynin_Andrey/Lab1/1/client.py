import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.sendto('Hello, server'.encode(), ('localhost', 6061))

data = sock.recv(1024)
sock.close()

print(data.decode())