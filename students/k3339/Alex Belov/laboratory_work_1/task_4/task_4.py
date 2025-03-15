import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
clients = []


def handle_client(client_socket, client_address):
    print(f"New connection: {client_address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"{client_address} said: {message}")

            broadcast_message(message, client_socket)
    except ConnectionResetError:
        print(f"{client_address} disconnected")
    finally:
        clients.remove(client_socket)
        client_socket.close()


def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started at {SERVER_HOST}:{SERVER_PORT}, waiting for clients...")

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input("You: ")
            client_socket.send(message.encode('utf-8'))
    finally:
        client_socket.close()


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\nNew message: {message}")
        except:
            print("Connection closed...")
            break


if __name__ == "__main__":
    role = input("Выберите режим (server/client): ").strip().lower()

    if role == 'server':
        start_server()
    elif role == 'client':
        start_client()