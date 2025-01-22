import socket
import threading

clients = []

def handle_client(client_socket, addr):
    print(f"Подключен клиент: {addr}")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"{addr}: {message}")
                broadcast(message, client_socket)
            else:
                remove(client_socket)
                break
        except:
            remove(client_socket)
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                remove(client)

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 4040))
server_socket.listen(5)

print("Сервер ожидает подключения...")

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
