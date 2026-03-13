import socket
import threading

HOST = "127.0.0.1"
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            print(client.recv(1024).decode())
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input()
    client.send(msg.encode())