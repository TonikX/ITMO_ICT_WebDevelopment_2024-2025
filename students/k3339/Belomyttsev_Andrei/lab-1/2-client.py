import socket

IP = '127.0.0.1'
PORT = 2020

print('Parallelogram Area Calculator')
x = input('Enter a, h or a, b, alpha: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.send(x.encode('utf-8'))
data = client.recv(1024)
print('Result:', data.decode())
client.close()