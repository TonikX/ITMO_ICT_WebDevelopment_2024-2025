import socket
import threading

clients: list[socket.socket] = []


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except OSError as e:
                raise KeyboardInterrupt from e


def get_messages(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                message = f"{address[0]}:{address[1]} says: " + message.decode()
                broadcast(message, client_socket)
            else:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            client_socket.close()
            clients.remove(client_socket)
            break


def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")
        clients.append(client_socket)

        client_thread = threading.Thread(target=get_messages, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    server_program()
