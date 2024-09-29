import socket

IP_ADDRESS = "127.0.0.1"
PORT = 4000
BUFFER = 1024

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.bind((IP_ADDRESS, PORT))

print("сервер запустился")

while True:
    data, addr = serv.recvfrom(BUFFER)
    print("Новое сообщение:", data.decode())
    serv.sendto("привет клиент".encode(), addr)