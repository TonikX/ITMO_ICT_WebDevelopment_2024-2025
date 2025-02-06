import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_ADDRESS = ("127.0.0.1", 1024)
MESSAGE = b"Hello, client!"
BUFFER_SIZE = 1024

print(f"Starting up on {SERVER_ADDRESS}")
server_socket.bind(SERVER_ADDRESS)

while True:
    print("Waiting to receive message..")
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Received message: {data}, from {client_address}")
    server_socket.sendto(MESSAGE, client_address)
    print(f"Sent message {MESSAGE} back to {client_address}")
