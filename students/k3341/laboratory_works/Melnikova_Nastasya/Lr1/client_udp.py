import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12345)

sock.sendto("Hello, server".encode(), server_address) # отправляем сообщение серверу

data, _ = sock.recvfrom(1024)
print("Ответ сервера:", data.decode())

sock.close()