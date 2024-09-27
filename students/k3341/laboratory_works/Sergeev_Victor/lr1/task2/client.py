import socket

HOST = '127.0.0.1'
PORT = 16000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
intro = client.recv(1024)
print(f'Client received: {intro.decode()}')

while True:
    try:
        payload = input('Input 3 numbers: ')
    except KeyboardInterrupt:
        print('Shutting client...')
        break
    try:
        data = payload.split()
        if len(data) != 3:
            print('Try harder!')
            continue
        numbers = map(int, data)
        client.sendall(payload.encode())
        print(f'Client sent: {payload}')
    except ValueError:
        print('Try harder!')
    
    try:
        data = client.recv(1024)
        print(f'Client received: {data.decode()}')
    except ConnectionResetError:
        print('Server fell...')

client.close()