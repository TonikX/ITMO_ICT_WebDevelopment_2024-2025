import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8080)

message = "Hello, server"
client_socket.sendto(message.encode(), server_address)
print(f"Отправлено сообщение серверу: {message}")

data, _ = client_socket.recvfrom(1024)
print(f"Получено сообщение от сервера: {data.decode()}")

client_socket.close()