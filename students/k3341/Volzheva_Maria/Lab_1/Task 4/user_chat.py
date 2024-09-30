import socket
import threading


def get_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'Enter your nickname: ':
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print('You have lost connection with server!')
            client.close()
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8081))

nickname = input('Enter your nickname: ')

thread = threading.Thread(target=get_messages)
thread.start()

while True:
    message = input()
    client.send(f'{nickname}: {message}'.encode())
