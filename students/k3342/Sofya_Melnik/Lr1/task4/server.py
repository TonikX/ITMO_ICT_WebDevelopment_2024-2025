from socket import socket, AF_INET, SOCK_STREAM
import threading

clients = {}
lock_clients = threading.Lock()

def broadcast(message: str, current_client: [socket, None]) -> None:
    for client in clients.keys():
        if current_client is None:
            output = f'system: {message}'
        elif client != current_client:
            output = f'{clients[current_client]}: {message}'
        else:
            continue
        with lock_clients:
            client.send(output.encode())


def handle_client(client_socket: socket):
    name = client_socket.recv(1024).decode()
    with lock_clients:
        clients[client_socket] = name

    broadcast(f"New user spotted: {name}", current_client=None)

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                broadcast(message, current_client=client_socket)
            else:
                break
    finally:
        with lock_clients:
            del clients[client_socket]
        client_socket.close()
        broadcast(f"{name} left :(", current_client=None)


def start_server(socket_address: tuple[str, int] = ('localhost', 20777)) -> None:
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(socket_address)
    server.listen()

    print(f"Server listening on {':'.join(map(str, socket_address))}")

    while True:
        try:
            client_socket, client_address = server.accept()
            print(f"New connection: {client_address}")

            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        except KeyboardInterrupt:
            server.close()
            break


if __name__ == "__main__":
    start_server()