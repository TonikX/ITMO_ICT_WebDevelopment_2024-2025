import socket

IP = "127.0.0.1"
PORT = 4000
BUFFER = 1024
MSG = "Hello, server"

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.bind((IP, PORT))

print("Server started!")

while True:
    data, addr = serv.recvfrom(BUFFER)
    print("New message:", data.decode())
    serv.sendto("Hello, client".encode(), addr)