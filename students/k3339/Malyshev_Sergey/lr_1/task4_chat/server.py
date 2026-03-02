import socket
import threading

HOST = 'localhost'
PORT = 9090

clients = []     # список сокетов клиентов
nicknames = []   # список никнеймов


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()

                nickname = nicknames[index]
                nicknames.remove(nickname)

                broadcast(f"{nickname} left the chat.".encode('utf-8'))
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Server started, waiting for connections...")

    while True:
        client, address = server.accept()
        print(f"Connected: {address}")

        client.send('nickname'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        clients.append(client)
        nicknames.append(nickname)

        print(f"Client nickname: {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("You are connected to the chat!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()
