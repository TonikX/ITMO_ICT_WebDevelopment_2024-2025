import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 1937)

message = "Hello, server"
client.sendto(message.encode(), server_address)

data, sender_addr = client.recvfrom(1024)
print("Message from server:", data.decode())
client.close()