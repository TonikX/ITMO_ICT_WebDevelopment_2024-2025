import socket

IP = 'localhost'
PORT = 8080

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((IP, PORT))

a = float(input('Длина: '))
h = float(input('Высота: '))
data = f'{a},{h}'
client_sock.send(data.encode())
response = client_sock.recv(1024).decode()
print(f'Площадь параллелограмма {response}')
client_sock.close()