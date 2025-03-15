import socket

socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 8088)
socket_server.bind(server_address)

while True:
    data, address = socket_server.recvfrom(1024)
    print(f"Сообщение от клиента {address}: {data.decode()}")

    response = "Hello, client"
    socket_server.sendto(response.encode(), address)
