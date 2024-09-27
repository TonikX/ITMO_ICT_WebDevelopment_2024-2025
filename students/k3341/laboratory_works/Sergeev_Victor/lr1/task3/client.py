import socket

HOST = '127.0.0.1'
PORT = 16000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

responce = client.recv(4096).decode()
print(f'Client received:\n{responce}')
client.close()

