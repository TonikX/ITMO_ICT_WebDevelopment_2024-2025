import socket
import threading

HOST = '127.0.0.1'
PORT = 65433

clients = {}
addresses = {}

def handle_client(client_socket, client_address):
    name = client_socket.recv(1024).decode()
    welcome_message = f"Привет, {name}! Если вы хотите выйти, введите 'exit'."
    client_socket.send(bytes(welcome_message, "utf-8"))
    message = f"{name} присоединился"
    broadcast(bytes(message, "utf-8"))
    clients[client_socket] = name
    addresses[client_socket] = client_address

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, name+": ")
            else:
                remove(client_socket)
        except:
            continue

def broadcast(message, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf-8")+message)

def remove(client_socket):
    name = clients[client_socket]
    del clients[client_socket]
    del addresses[client_socket]
    message = f"{name} покинул чат"
    broadcast(bytes(message, "utf-8"))

def connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Сервер запущен и ожидает подключения...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент {client_address}")
            client_socket.send(bytes("Введите ваше имя: ", "utf-8"))
            addresses[client_socket] = client_address
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    connection()


