import socket
import threading

members = {}  # nickname: client_socket


def start_chat(sock):
    while True:
        client_socket, client_address = sock.accept()
        print("Got connection from", client_address)

        threading.Thread(target=handle_clients, args=(client_socket,)).start()


def sending_messages(message, nick):
    for nickname in members.keys():
        if nickname != nick:
            members[nickname].sendall(message.encode())


def handle_clients(client):
    client.send("Enter your nickname to join the chat".encode())
    nickname = client.recv(1024).decode()
    members[nickname] = client
    sending_messages(f"New user joined: {nickname}", nickname)

    while True:
        try:
            message = client.recv(1024).decode()
            sending_messages(message, nickname)
        except Exception as error:
            client.sendall(f"This error occurred: {error}".encode())


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 2024))
    sock.listen(5)
    print("Server listening on port 2024")

    start_chat(sock)


if __name__ == '__main__':
    run()
