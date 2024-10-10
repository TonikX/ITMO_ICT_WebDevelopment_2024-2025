import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Hello, server"

sock.sendto(message.encode(), ('localhost', 2024))
data, server = sock.recvfrom(1024)
print(data.decode())

sock.close()
