import socket
import threading

clients = {}

def broadcast(message, sender_socket=None):
    for client, name in clients.items():
        if client != sender_socket:
                client.send(message.encode('utf-8'))


def handle_client(client_socket):
    client_socket.send("Введите своё имя: ".encode('utf-8'))
    client_name = client_socket.recv(1024).decode('utf-8').strip()
    clients[client_socket] = client_name
    print(f"{client_name} подключился.")

    broadcast(f"{client_name} присоединился к чату!", sender_socket=client_socket)

    while True:
        message = client_socket.recv(1024).decode('utf-8').strip()
        if not message:
            break
        print(f"{client_name}: {message}")
        broadcast(f"{client_name}: {message}", sender_socket=client_socket)


def start_server(host='127.0.0.1', port=5555):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Новое подключение: {client_address}")

        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()


if __name__ == "__main__":
    start_server()
