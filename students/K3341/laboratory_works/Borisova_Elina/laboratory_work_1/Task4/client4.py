import socket
import threading

def receive_messages(socket):
    while True:
        try:
            message = socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Disconnect")
            socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8080))
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            client.close()
            break
        client.send(message.encode('utf-8'))
start_client()