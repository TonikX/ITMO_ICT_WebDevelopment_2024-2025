import socket
import threading

clients = []
client_names = []


def broadcast(message, sender):
    """Функция для отправки сообщения всем клиентам, кроме отправителя"""
    for client in clients:
        if client != sender:
            client.send(message)


def handle_client(client_socket, client_address):
    """Функция для обработки клиентов"""
    print(f"[{client_address}] подключился.")

    client_socket.send("Введите ваше имя: ".encode('utf-8'))
    client_name = client_socket.recv(1024).decode('utf-8')
    clients.append(client_socket)
    client_names.append(client_name)

    welcome_message = f"{client_name} присоединился к чату!".encode('utf-8')
    broadcast(welcome_message, client_socket)

    try:
        while True:
            message = client_socket.recv(1024)
            if message:
                full_message = f"{client_name}: {message.decode('utf-8')}".encode('utf-8')
                broadcast(full_message, client_socket)
            else:
                break
    finally:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        client_names.pop(index)
        client_socket.close()
        print(f"[{client_address}] отключился.")
        broadcast(f"{client_name} покинул чат.".encode('utf-8'), client_socket)


def start_server():
    """Функция для запуска сервера"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen()

    print("[Сервер запущен] Ожидание подключения клиентов...")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    start_server()
