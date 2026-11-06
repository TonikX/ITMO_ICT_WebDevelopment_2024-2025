import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 12345))

print("Сервер запущен. Ожидание сообщения...")

data, address = server.recvfrom(1024)
print(data.decode())

server.sendto("Hello, client".encode(), address)
server.close()