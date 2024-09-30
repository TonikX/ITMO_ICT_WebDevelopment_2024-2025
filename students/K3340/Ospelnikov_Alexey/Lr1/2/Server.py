import socket
import math

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(('', 8080))

max_user = 1
while True:
    
    client_data, addr = socket.recvfrom(1024)
    if not client_data:
        break
    if len(client_data.split()) != 3:
        socket.sendto(b"Wrong Input", addr)
    else:
        parall_measures = client_data.split()
        S = float(parall_measures[0]) * float(parall_measures[1]) * math.sin(float(parall_measures[2]))
        socket.sendto(bytes(str(S), "utf-8"), addr)
    print(client_data)

socket.close()
    
