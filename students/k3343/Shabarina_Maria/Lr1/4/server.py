import socket
import threading

clients = {}


def new_client(connection, address):
    print(f"New connection: {address}")
    connection.send("Welcome! Enter your name or nickname: ".encode())
    name = connection.recv(1024).decode()
    clients[connection] = name
    if len(clients.values()) == 1:
        connection.send(f"Hello, {name}!".encode())
    else:
        connection.send(f"Hello, {name}! {', '.join(clients.values())} are in the chat".encode())
    send_to_all(f"{name} is online", connection)
    while True:
        try:
            message = connection.recv(1024).decode()
            if not message:
                break
            send_to_all(f"{name}: {message}", connection)
        except:
            break
    connection.close()
    del clients[connection]
    client_left(name)
    print(f"Closed connection: {address}")


def client_left(name):
    for client in clients:
        try:
            client.send(f"{name} left chat".encode())
        except:
            break


def send_to_all(message, sender_connection):
    for client in clients:
        if client != sender_connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.pop(client)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 1234))
server_socket.listen()
print("Server started")
while True:
    client_connection, client_address = server_socket.accept()
    thread = threading.Thread(target=new_client, args=(client_connection, client_address))
    thread.start()
