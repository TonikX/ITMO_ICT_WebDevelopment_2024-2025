import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(('', 8080))

max_user = 1
response = b"Hello, client"

while True:
    client_data, addr = socket.recvfrom(1024)
    if not client_data:
        break
    print(client_data)
    socket.sendto(response, addr)

socket.close()
    
