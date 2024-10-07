import socket
import threading

clients = []
client_names = {}


def handle_client(client_socket, addr):
    client_socket.send("Введите ваше имя: ".encode())
    name = client_socket.recv(1024).decode()
    client_names[client_socket] = name

    print(f"Новое соединение: {addr} ({name})")
    broadcast(f"{name} присоединился к чату!", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"{name} ({addr}): {message}")
            broadcast(f"{name}: {message}", client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            broadcast(f"{name} покинул чат.", client_socket)
            break


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

print("Сервер запущен и ожидает клиентов...")

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()