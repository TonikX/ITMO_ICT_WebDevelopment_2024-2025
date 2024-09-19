import socket

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print("Server is running")

while True:
    data, client_address = server.recvfrom(BUFFER_SIZE)
    decoded_data = data.decode()
    print(decoded_data)
    server.sendto("Hello, client".encode(), client_address)
    if decoded_data == "stop_server":
        break
server.close()
