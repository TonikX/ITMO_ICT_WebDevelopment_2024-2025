import socket

HOST = (socket.gethostname(), 8000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(HOST)

while True:

    data, client_address = server_socket.recvfrom(1024)

    print(f"Получено сообщение: {data.decode()} от {client_address}")

    server_socket.sendto("Hello, client".encode(), client_address)
