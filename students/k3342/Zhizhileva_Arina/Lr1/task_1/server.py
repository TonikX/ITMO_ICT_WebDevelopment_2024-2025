from socket import *

server_socket = socket(AF_INET, SOCK_DGRAM)
server_address = ('localhost', 12345)

server_socket.bind(server_address)

print("UDP is running")

while True:
    print("waiting for data...")
    data, client_address = server_socket.recvfrom(1024)
    if not data:
        break
    print(f"Message from client '{data.decode()}' was received from client.", flush=True)

    response = "Hello, client!"
    server_socket.sendto(response.encode(), client_address)
    print(f"Message '{response}' was sent to client.")

server_socket.close()

