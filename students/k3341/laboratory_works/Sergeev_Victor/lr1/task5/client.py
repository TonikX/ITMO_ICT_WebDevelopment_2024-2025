import socket
from colorama import init, Fore
init()

HOST = '127.0.0.1'
PORT = 16000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

request = f'''\
GET /subjects HTTP/1.1\r\n\
Host: {HOST}:{PORT}\r\n\
Connection: close\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Content-Length: 28\r\n\r\n\
math=5&math=5&math=4&web=100
'''

client.sendall(request.encode())
print(f'{Fore.YELLOW}Client sent:\n{Fore.WHITE}{request}{Fore.RESET}')
responce = client.recv(1024).decode()
print(f'{Fore.YELLOW}Client received:\n{Fore.WHITE}{responce}{Fore.RESET}')

client.close()
