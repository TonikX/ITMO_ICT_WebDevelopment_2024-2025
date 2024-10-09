import socket

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode(), (HOST, PORT))

response, server_address = client.recvfrom(BUFFER_SIZE)
decoded_data = response.decode()
print(decoded_data)

client.close()
