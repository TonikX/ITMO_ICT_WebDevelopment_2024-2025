import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 8080
ENCODING = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except OSError:  # Handles socket errors
            if client in clients:
                disconnect_client(client)
            break


def disconnect_client(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    nicknames.remove(nickname)
    broadcast(f'{nickname} left!'.encode(ENCODING))


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('margo'.encode(ENCODING))
        nickname = client.recv(1024).decode(ENCODING)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode(ENCODING))
        client.send('Connected to server!'.encode(ENCODING))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == "__main__":
    print(f"Server running on {SERVER_HOST}:{SERVER_PORT}")
    receive()
