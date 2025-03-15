import socket

HOST = '127.0.0.1'
PORT = 16000
intro = b'Here\'s my Trapezoid square-computing server\nPls input both bases and height to get a square'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

while True:
    try:
        client, _ = server.accept()
        print(f'Server sent: {intro.decode()}')
        client.sendall(intro)
    except KeyboardInterrupt:
        print('Shutting server')
        break
    while True:
        try:
            data = client.recv(1024).decode()
            print(f'Server received: {data}')
            data = list(map(int, data.split()))
            square = round((data[0] + data[1]) * data[2] / 2, 2)
            client.sendall(b'Server sent: Your square: '+ str(square).encode())
        except (ConnectionResetError, IndexError):
            print('Client shutted')
            client = None
            break
    try:
        pass
    except KeyboardInterrupt:
        print()
        break

server.close()
