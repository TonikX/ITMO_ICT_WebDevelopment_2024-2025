import socket
import math

IP = '127.0.0.1'
PORT = 2020

def calc(x):
  try:
    x = list(map(float, x.split()))
  except:
    return 'Wrong format'
  if len(x) == 2:
    a, h = x
    return str(a * h)
  elif len(x) == 3:
    a, b, alpha = x
    return str(a * b * math.sin(math.radians(alpha)))
  else:
    return 'Wrong format'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
client, address = server.accept()
data = client.recv(1024).decode('utf-8')
client.send(calc(data).encode('utf-8'))
client.shutdown(socket.SHUT_WR)
server.close()