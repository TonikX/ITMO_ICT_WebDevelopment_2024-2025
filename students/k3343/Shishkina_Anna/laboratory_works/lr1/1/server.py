import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 12345))

print("Сервер запущен...")

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f"{message.decode('utf-8')}")

    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), client_address)

server_socket.close()