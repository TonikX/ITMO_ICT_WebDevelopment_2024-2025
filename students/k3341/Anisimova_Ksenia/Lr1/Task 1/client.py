import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), server_address)
response, _ = client_socket.recvfrom(1024)

print(f"Message from server: {response.decode('utf-8')}")

client_socket.close()