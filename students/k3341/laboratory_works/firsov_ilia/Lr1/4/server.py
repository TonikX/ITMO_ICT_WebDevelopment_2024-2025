import socket
import threading

clients: list[socket.socket] = []


def connect_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received message from {client_address}: {message}")

            broadcast(message, client_socket)
    finally:
        # removing client when disconnected
        clients.remove(client_socket)
        client_socket.close()
        print(f"Connection closed for {client_address}")


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                # removing client if sending fails
                clients.remove(client)
                client.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5551)
server_socket.bind(server_address)
server_socket.listen(5)

print("Server is running and waiting for connections...")

try:
    while True:
        client_socket, client_address = server_socket.accept()

        # start a new thread for each client
        client_thread = threading.Thread(target=connect_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("Exiting")
    for s in clients:
        s.close()
    server_socket.close()
