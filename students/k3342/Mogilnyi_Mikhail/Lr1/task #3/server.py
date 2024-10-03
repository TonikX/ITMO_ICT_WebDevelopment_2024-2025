import socket

HOST = '0.0.0.0'
PORT = 1313

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

while True:
    client, addr = server.accept()
    print(f'Connection from {addr}')

    request = client.recv(1024).decode()
    print(f'Client request:\n{request}')

    with open('index.html', 'r') as file:
        content = file.read()

    response = 'HTTP/1.0 200 OK\n\n' + content

    client.sendall(response.encode())

server.close()