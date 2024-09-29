import socket
import threading

HOST = '127.0.0.1'
PORT = 8080


def receive_messages(server):
    while True:
        data = server.recv(1024).decode()
        print(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=receive_messages, args=(s,)).start()
    while True:
        message = input()
        if message.lower() == 'exit':
            s.close()
            break
        s.send(message.encode())
