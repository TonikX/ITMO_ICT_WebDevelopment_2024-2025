import sys
import socket

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()


getting_data = True
while getting_data:
    message = bytes(input(), 'utf-8')
    client_socket.sendto(message, ('localhost', 8080))
    serv_response = client_socket.recv(1024)
    if not serv_response:
        client_socket.close()
        break
    print(serv_response)

