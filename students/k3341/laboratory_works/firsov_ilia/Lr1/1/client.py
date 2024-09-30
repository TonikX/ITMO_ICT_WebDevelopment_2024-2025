import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)

message = "Hello, server"
client_socket.sendto(message.encode(), server_address)

response, server = client_socket.recvfrom(1024)
print(f"Server response: {response.decode()}")

# Закрываем соединение
client_socket.close()
