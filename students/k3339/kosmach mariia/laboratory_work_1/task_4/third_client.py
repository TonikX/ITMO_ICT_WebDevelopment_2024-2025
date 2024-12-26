import socket
import threading

server_address = ('localhost', 14900)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

def listen():
    while True:
        data = client.recv(16384)
        print(data.decode('UTF-8'))

def polling():
    while True:
        data = input()
        client.send(data.encode('utf-8'))


listen_thread = threading.Thread(target=listen)
listen_thread.start()

polling_thread = threading.Thread(target=polling)
polling_thread.start()

