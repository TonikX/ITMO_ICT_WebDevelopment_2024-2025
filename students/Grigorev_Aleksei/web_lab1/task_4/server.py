import socket
import threading


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024


clients = []

def handle_client(client_socket, address):
    """Обрабатывает отдельного клиента."""
    print(f"Подключен клиент: {address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if not message:
                break
            print(f"Сообщение от {address}: {message}")

            broadcast(message, client_socket)
    except ConnectionResetError:
        print(f"Клиент {address} отключился.")
    finally:
        clients.remove(client_socket)
        client_socket.close()

def broadcast(message, sender_socket):
    """Рассылает сообщение всем клиентам, кроме отправителя."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def tcp_server():
    """Запуск TCP-сервера."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()
        print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
            thread.start()

if __name__ == "__main__":
    tcp_server()
