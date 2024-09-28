import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = []


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            index = clients.index(client)
            clients.remove(client)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break


def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f'Сервер слушает {HOST}:{PORT}')

    while True:
        client, address = server.accept()
        print(f'Подключен {str(address)}')

        clients.append(client)

        client.send('NICK'.encode('utf-8'))
        nick = client.recv(1024).decode('utf-8')

        broadcast(f'{nick} присоединился к чату!'.encode('utf-8'))

        client.send('Вы подключены к чату!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Сервер запущен...')
receive()
