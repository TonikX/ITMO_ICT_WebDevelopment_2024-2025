import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)

message = "Hello, server"

with client_socket:
    client_socket.sendto(message.encode(), server_address)
    print(f"Сообщение отправлено серверу: {message}")

    response, _ = client_socket.recvfrom(1024)
    print(f"Получено сообщение от сервера: {response.decode()}")
