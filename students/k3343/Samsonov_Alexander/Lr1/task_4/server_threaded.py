import socket
import threading

clients = {}
clients_lock = threading.Lock()


def broadcast(message, current_client):
    for client in clients.keys():
        if current_client is None:
            output = f'system: {message}'
        elif client != current_client:
            output = f'{clients[current_client]}: {message}'
        else:
            continue
        with clients_lock:
            client.send(output.encode())


def handle_client(client_socket):
    name = client_socket.recv(1024).decode()
    with clients_lock:
        clients[client_socket] = name

    welcome_message = f"{name} has joined the chat!"
    broadcast(welcome_message, current_client=None)

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                broadcast(message, current_client=client_socket)
            else:
                break
    finally:
        with clients_lock:
            del clients[client_socket]
        client_socket.close()
        broadcast(f"{name} has left the chat.", current_client=None)


def start_server(socket_address: tuple[str, int] = ('localhost', 12345)):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(socket_address)
    server.listen()

    print(f'Server listening on {':'.join(map(str, socket_address))}...')

    while True:
        try:
            client_socket, client_address = server.accept()
            print(f"New connection from {client_address}")

            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        except KeyboardInterrupt:
            server.close()
            break


if __name__ == "__main__":
    start_server()
