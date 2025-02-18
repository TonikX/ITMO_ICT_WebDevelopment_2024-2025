import socket
import threading

clients = []


def handle_client(client_socket):
    clients.append(client_socket)
    while True:
        message = client_socket.recv(1024)
        if message.decode().lower() == 'exit' :
            clients.remove(client_socket)
            continue
        message = f"User{str(client_socket).split(',')[0][18:]}: {message.decode()}".encode()
        broadcast(message, client_socket)


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)


def start_server(host='localhost', port=8083):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is running on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
