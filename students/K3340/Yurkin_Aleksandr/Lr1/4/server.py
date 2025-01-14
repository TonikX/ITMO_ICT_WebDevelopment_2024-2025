import socket
import threading

IP = "127.0.0.1"
PORT = 1234
BUFFER = 1024

users = {}

def send_message(sock, msg):
    for user in users:
        if user != sock:
            user.send(f'{users[sock]}: {msg}'.encode())

def handler(sock):
    while True:
        msg = sock.recv(BUFFER).decode()
        if msg == 'quit':
            users.pop(sock)
            break
        send_message(sock, msg)


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))

print("Server started!")

serv.listen(10)

while True:
    sock, _ = serv.accept()
    nickname = sock.recv(BUFFER).decode()
    users[sock] = nickname
    thread = threading.Thread(target=handler, args=(sock,))
    thread.start()
