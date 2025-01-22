import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = 'localhost'
PORT = 8080
address = HOST, PORT
message = "Hi, UDP server!"

s.sendto(message.encode(), address)
print(f"Sent message to server: {message}")

response, server_address = s.recvfrom(1024)
print(f"Got reply from server: {response.decode()}")
s.close()
