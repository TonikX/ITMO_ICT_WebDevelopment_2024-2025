import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = []
name_map = {}


def handle_client(conn, addr):
    print(f"New connection from {addr}")
    conn.send("Welcome to the chat! Enter your name!".encode())
    name = conn.recv(1024).decode()
    name_map[conn] = name
    conn.send(f"Hello, {name}!".encode())
    broadcast("joined the server", conn)
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            broadcast(message, conn)
        except:
            break
    conn.close()
    name_map.pop(conn)
    clients.remove(conn)
    print(f"Connection closed from {addr}")


def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(f"{name_map[sender_conn]}: {message}".encode())
            except:
                client.close()
                clients.remove(client)
                name_map.pop(client)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Chat server started on port", PORT)
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
