import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 65432))

while True :
    data, address = sock.recvfrom(1024)
    print(f'Получено сообщение от {address}: {data.decode()}')

    response = 'Hello, client'
    sock.sendto(response.encode(), address)