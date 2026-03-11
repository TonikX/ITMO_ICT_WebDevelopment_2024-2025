import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12347))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            print(msg)
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input()
    client.send(msg.encode())
