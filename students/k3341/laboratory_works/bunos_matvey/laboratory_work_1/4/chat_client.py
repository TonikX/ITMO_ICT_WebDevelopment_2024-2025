import socket
import threading

HOST = '127.0.0.1'
PORT = 65432


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024)
            if not message:
                break
            print(message.decode())
        except:
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=receive_messages, args=(s,)).start()
    while True:
        message = input()
        if message.lower() == 'exit':
            s.close()
            break
        s.send(message.encode())
