import socket

HOST = '127.0.0.1'
PORT = 16000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

while True:
    try:
        data, addr = server.recvfrom(1024)
        print(f'Server received: {data.decode()}')
        server.sendto(b'Hello client', addr)
        print(f'Server sent: Hello client')
    except Exception:
        break

server.close()