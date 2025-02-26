import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 1234))
print("Сервер запущен, ожидает подключения...")

conn, addr = server.recvfrom(1024)
request = conn.decode()
print(f'Запрос от {addr}: {request}')

response = 'Hello client'
server.sendto(response.encode(), addr)

server.close()