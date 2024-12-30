import socket
import threading

HOST = 'localhost'
PORT = 9801
maxUsers = 10

clients = []
usernames = {}


#send message for all people
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)


def handler(client_socket):
    username = client_socket.recv(1024).decode('utf-8')
    usernames[client_socket] = username
    welcome_message = f"{username} joined the chat room!".encode('utf-8')
    broadcast(welcome_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            if message.decode('utf-8') == "/exit":
                print(f"{usernames[client_socket]} disconnected")
                clients.remove(client_socket)
                client_socket.close()
                broadcast(f"{usernames[client_socket]} exited the chat room".encode('utf-8'), client_socket)
                del usernames[client_socket]
                break
            else:
                full_message = f"{usernames[client_socket]}: {message.decode('utf-8')}".encode('utf-8')
                broadcast(full_message, client_socket)
        except:
            print(f"{usernames[client_socket]} disconnected")
            clients.remove(client_socket)
            client_socket.close()
            broadcast(f"{usernames[client_socket]} exited the chat room".encode('utf-8'), client_socket)
            del usernames[client_socket]
            break


def start_server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(maxUsers)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = serverSocket.accept()
        print(f"Connection from {client_address}")
        clients.append(client_socket)
        thread = threading.Thread(target=handler, args=(client_socket,))
        thread.start()


start_server()