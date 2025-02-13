import socket
import threading

clients = {}

def broadcast(message, sender_socket):
    for client_socket, client_name in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket):
    try:
        client_name = client_socket.recv(1024).decode()
        clients[client_socket] = client_name
        print(f"{client_name} подключился к чату.")
        broadcast(f"{client_name} присоединился к чату.", client_socket)

        while True:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"{client_name}: {message}")
                broadcast(f"{client_name}: {message}", client_socket)
            else:
                break
    except:
        pass
    finally:
        print(f"{clients[client_socket]} отключился.")
        broadcast(f"{clients[client_socket]} покинул чат.", client_socket)
        client_socket.close()
        del clients[client_socket]

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Новое подключение от {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()