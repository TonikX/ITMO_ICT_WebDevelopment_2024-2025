import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(('localhost', 8080))

while True:
    data, addr = server_sock.recvfrom(1024)
    print(
        f'Получено сообщение "{data.decode("utf-8")}" от адреса'
        f' {addr}'
    )
    reply = b'Hello, Client!'
    server_sock.sendto(reply, addr)


