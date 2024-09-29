import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = 'Hello, server'
sock.sendto(message.encode(), ('127.0.0.1', 65432))

data, address = sock.recvfrom(1024)
print(f'Получено сообщение от {address}: {data.decode()}')