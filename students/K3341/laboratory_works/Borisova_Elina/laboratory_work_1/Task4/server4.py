import socket
import threading

clients = []
def handle_client(socket, address):
    print(f"New connection: {address}")

    while True:
        try:
            message = socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Message from {address}: {message}")
            broadcast(message, socket)
        except:
            break
    socket.close()
    clients.remove(socket)
    print(f"Member removed: {address}")
def broadcast(message, socket):
    for client in clients:
        if client != socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen()
    print("Server is started")
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

start_server()