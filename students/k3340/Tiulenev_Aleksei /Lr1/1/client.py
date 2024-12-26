import socket

IP = "127.0.0.1"
PORT = 4000
BUFFER = 1024
MSG = "Привет, сервер"

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.sendto(MSG.encode(), (IP, PORT))

data, _ = serv.recvfrom(BUFFER)
print("сообщение", data.decode())
