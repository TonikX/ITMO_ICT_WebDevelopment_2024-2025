import socket
import threading


clients = []
nicknames = []


def broadcast(message, client):
    for c in clients:
        if c != client:
            c.send(message)


def client_connection(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} not in chat now.'.encode(), client)
            nicknames.remove(nickname)
            break


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 8081))
server.listen()

print('Server is running and waiting for connection...')

while True:
    client, address = server.accept()
    print(f'Connect to  {str(address)}')

    client.send('Enter your nickname: '.encode())
    nickname = client.recv(1024).decode()
    nicknames.append(nickname)
    clients.append(client)

    print(f'Nickname of user: {nickname}')
    broadcast(f'{nickname} is in chat now!'.encode(), client)
    client.send('Welcome to the chat!'.encode())

    thread = threading.Thread(target=client_connection, args=(client,))
    thread.start()
