import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    message = bytes(input(), 'utf-8')
    socket.sendto(message, ('localhost', 8080))
    response = socket.recv(1024)
    if not response:
        break
    print(response)
socket.close()