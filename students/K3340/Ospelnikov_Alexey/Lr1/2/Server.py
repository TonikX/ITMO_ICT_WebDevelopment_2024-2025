import socket
import math

server_socket = socket.socket()
server_socket.bind(('', 8080))

max_user = 5
server_socket.listen(max_user)
while True:
    client_socket, addr = server_socket.accept()
    client_data = list(map(lambda x: int(x), client_socket.recv(1024).decode().split()))
    if not client_data or len(client_data) != 3:
        print("Invalid parameters for triangle area task")
        client_socket.close()
        break
    S = client_data[0] * client_data[1] * math.sin(client_data[2])
    client_socket.send(bytes(str(S), 'utf-8'))    
    print(client_data)

socket.close()
    
