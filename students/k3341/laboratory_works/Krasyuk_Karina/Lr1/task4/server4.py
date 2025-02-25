import socket
import threading

clients = []


def handle_client(client_socket, client_address):
    print(f"Новое соединение с адреса - {client_address}")
    client_socket.send("Введите имя: ".encode())
    username = client_socket.recv(1024).decode()

    clients.append(client_socket)

    print(f"{username} присоединился к чату")
    broadcast(f"{username} присоединился к чату", client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(f"{username}: {message.decode()}", client_socket)
            else:
                break
        except:
            break

    remove_client(client_socket)
    broadcast(f"{username} покинул чат", client_socket)


def remove_client(client):
    clients.remove(client)
    client.close()


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', 8080))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
