import socket
import threading

HOST = '127.0.0.1'
PORT = 65433

def receive_message(socket):
    while True:
        try:
            message = socket.recv(1024)
            if not message:
                break
            print(message.decode())
        except:
            break

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        threading.Thread(target=receive_message, args=(s,)).start()
        while True:
            message = input()
            if message == 'exit':
                s.close()
                break
            s.send(message.encode())

if __name__ == "__main__":
    connection()
