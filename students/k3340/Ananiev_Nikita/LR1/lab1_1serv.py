import sys
import socket

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_socket.bind(('', 8080))

max_user_conn, listening = 1, True
serv_response = b"Hello, client"

while listening:
    client_data, addr = serv_socket.recvfrom(1024)
    if not client_data:
        break
    print(client_data)
    serv_socket.sendto(serv_response, addr)

serv_socket.close()
