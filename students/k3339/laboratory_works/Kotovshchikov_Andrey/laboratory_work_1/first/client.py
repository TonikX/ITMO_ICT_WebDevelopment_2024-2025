import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 8000
BUFFER_SIZE = 1024


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello server".encode(), (SERVER_HOST, SERVER_PORT))

response_data, server_address = client.recvfrom(BUFFER_SIZE)
decoded_data = response_data.decode()
print(decoded_data)

client.close()
