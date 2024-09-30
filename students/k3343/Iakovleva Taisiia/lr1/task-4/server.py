import socket
import threading

clients = []

HOST = 'localhost'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()
print(f"HTTP сервер запущен на {HOST}:{PORT}...")

def handle_client(client_connection, client_address):
    client_port = client_address[1]
    print(f"Новое подключение: {client_port}")
    while True:
        try:
            message = client_connection.recv(1024).decode()
            if message:
                print(f"Сообщение от {client_port}: {message}")
                broadcast_message(f"{client_port}: {message}", client_connection)
            else:
                remove_client(client_connection)
                break
        except:
            remove_client(client_connection)
            break

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                remove_client(client)

def remove_client(client_connection):
    if client_connection in clients:
        clients.remove(client_connection)
        client_connection.close()

while True:
    client_connection, client_address = server_socket.accept()
    clients.append(client_connection)

    thread = threading.Thread(target=handle_client, args=(client_connection, client_address))
    thread.start()
