import socket
import threading

IP = '127.0.0.1'
PORT = 2020

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

clients = []
names = []

def broadcast(message):
  for i in clients:
    i.send(message)

def handle(client):
  while True:
    try:
      index = clients.index(client)
      name = names[index]
      message = client.recv(1024)
      broadcast(message)
    except:
      clients.remove(client)
      client.close()
      broadcast(f'{name} left the chat.'.encode('utf-8'))
      names.remove(name)
      break

def connect():
  while True:
    client, address = server.accept()
    print(address, 'connected')
    client.send('NAME'.encode('utf-8'))
    name = client.recv(1024).decode('utf-8')
    names.append(name)
    clients.append(client)
    print('Name is', name)
    broadcast(f'{name} joined the chat.'.encode('utf-8'))
    threading.Thread(target=handle, args=(client,)).start()

print('Chat started...')
connect()