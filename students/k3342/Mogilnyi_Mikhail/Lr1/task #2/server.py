import socket
import math

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

def find_hypotenuse(leg_1, leg_2):
    hypotenuse = math.sqrt(float(leg_1) ** 2 + float(leg_2) ** 2)
    return hypotenuse

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

while True:
    client, addr = server.accept()
    data = client.recv(BUFFER_SIZE).decode()
    leg_1, leg_2 = data.split(',')
    answer = find_hypotenuse(leg_1, leg_2)
    client.send(str(answer).encode())
