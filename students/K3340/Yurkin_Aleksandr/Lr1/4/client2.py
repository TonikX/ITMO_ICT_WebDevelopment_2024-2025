import socket
import threading
import time

IP = "127.0.0.1"
PORT = 1234
BUFFER = 1024
NAME = 'Client 2'

def read_message(serv):
    while True:
        message = serv.recv(1024).decode()
        print(message)


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((IP, PORT))
threading.Thread(target=read_message, args=(serv,)).start()
serv.send(NAME.encode())

while True:
    serv.send(('Hello ' + str(time.time())).encode())
    time.sleep(1)
