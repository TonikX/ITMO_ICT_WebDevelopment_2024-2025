import socket
from threading import Thread


def receive_message(sock):
    while True:
        try:
            message = sock.recv(1024)
            if not message:
                break
            print(message.decode())
        except:
            break


con_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con_client.connect(('localhost', 6090))
accept_thread = Thread(target=receive_message, args=(con_client,)).start()
while True:
    message = input()
    con_client.send(message.encode())

