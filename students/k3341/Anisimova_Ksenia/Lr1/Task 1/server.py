import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Server is waiting for a client...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f"Message from client: {data.decode('utf-8')}")
    response_message = "Hello, client"
    server_socket.sendto(response_message.encode('utf-8'), client_address)