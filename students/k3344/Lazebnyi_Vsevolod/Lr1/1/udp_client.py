import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_address = ('localhost', 8080)
try:
    client_socket.sendto("Hello, server!".encode(), client_address)
    server_message, server_address = client_socket.recvfrom(1024)
    print(f"Получено сообщение от сервера: {server_message.decode()}")
finally:
    client_socket.close()