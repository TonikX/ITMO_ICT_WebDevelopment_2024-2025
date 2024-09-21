import sys
import socket

try:
    client_sock = socket.socket()
except socket.error:
    print('Failed to create socket')
    sys.exit()

# getting_response = True

client_sock.connect(('localhost', 4242))
print("Please write the lengths of triangle sides:")
client_sock.send(bytes(input(), 'utf-8'))
res = client_sock.recv(1024)
print(f"Area = {res.decode()}")
client_sock.close()
