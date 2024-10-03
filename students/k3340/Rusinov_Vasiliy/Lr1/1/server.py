import socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 14900)
server_sock.bind(server_address)

print("Сервер запущен и ожидает сообщения...")
while True:
    data, client_address = server_sock.recvfrom(1024)
    print(f"Сообщение от клиента: {data.decode()}")
    response = "Hello, client"
    server_sock.sendto(response.encode(), client_address)
