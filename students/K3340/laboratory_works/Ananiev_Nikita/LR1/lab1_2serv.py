import sys
import socket
import math

try:
    serv_socket = socket.socket()
    serv_socket.bind(('', 4242))
except socket.error:
    print('Failed to create socket')
    sys.exit()

max_conn_count, listening = 5, True

serv_socket.listen(max_conn_count)

while listening:
    client_socket, addr = serv_socket.accept()
    client_data = list(map(lambda x: int(x), client_socket.recv(1024).decode().split()))
    if not client_data or len(client_data) != 3:
        print("Invalid parameters for triangle area task")
        client_socket.close()
        break
    a, b, c = tuple(client_data)
    p = (a + b + c) / 2
    area = str(math.sqrt(p * (p - a) * (p - b) * (p - c)))
    client_socket.send(bytes(area, 'utf-8'))
