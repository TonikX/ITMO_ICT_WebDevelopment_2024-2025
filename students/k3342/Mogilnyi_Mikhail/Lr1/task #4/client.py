import socket
import threading

PORT = 1313
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 1024


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def client_receive():
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode()
            print(message)
        except:
            print('Error')
            client.close()
            break

def client_send():
    while True:
        message = f'{input()}'
        client.send(message.encode(FORMAT))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()