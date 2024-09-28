import socket
import threading

IP = '127.0.0.1'
PORT = 2020

name = input('Enter name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

def get():
  while True:
    try:
      message = client.recv(1024).decode('utf-8')
      if message == 'NAME':
        client.send(name.encode('utf-8'))
      else:
        print(message)
    except Exception as e:
      print(e)
      client.close()
      break

def send():
  while True:
    message = input()
    client.send(message.encode('utf-8'))

threading.Thread(target=get).start()
threading.Thread(target=send).start()