import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the server!'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected with: {str(address)}")

        client_socket.send('YOU_HAVE_JOINED_THE_CHAT!'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client_socket)

        print(f"Client nickname is {nickname}")
        broadcast(f"{nickname} joined the server!".encode('utf-8'))
        client_socket.send('Conected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


print("Server is listening")
receive()