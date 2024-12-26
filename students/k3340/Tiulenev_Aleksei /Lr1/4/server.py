import socket
import threading

HOST = "127.0.0.1"
PORT = 1234
BUFFER_SIZE = 1024

clients = {}

def broadcast_message(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(f'{clients[sender_socket]}: {message}'.encode('utf-8'))
            except:
                client_socket.close()
                if client_socket in clients:
                    del clients[client_socket]

def client_handler(client_socket):
    try:
        username = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
        if not username:
            client_socket.close()
            return
        clients[client_socket] = username
        print(f"{username} подключился.")
        broadcast_message(client_socket, "вошёл в чат.")

        while True:
            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
            message = data.strip()
            if message.lower() == 'quit':
                print(f"{username} отключился.")
                broadcast_message(client_socket, "вышел из чата.")
                client_socket.close()
                del clients[client_socket]
                break
            broadcast_message(client_socket, message)
    except:
        if client_socket in clients:
            print(f"{clients[client_socket]} отключился.")
            broadcast_message(client_socket, "вышел из чата.")
            client_socket.close()
            del clients[client_socket]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

print("Сервер запущен!")

server_socket.listen(10)

while True:
    client_socket, client_address = server_socket.accept()
    threading.Thread(target=client_handler, args=(client_socket,)).start()
