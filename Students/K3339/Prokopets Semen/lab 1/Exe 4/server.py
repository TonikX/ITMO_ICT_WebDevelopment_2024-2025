import socket
import threading

# Настройки сервера
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002

client_sockets = {}
usernames = {}


def handle_client(client_socket):
    # Запрашиваем имя пользователя
    client_socket.send("Введите ваше имя: ".encode())
    username = client_socket.recv(1024).decode()

    # Сохраняем имя пользователя
    usernames[client_socket] = username
    client_sockets[client_socket] = username

    # Уведомляем всех о новом пользователе
    broadcast(f"{username} присоединился к чату!", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                full_message = f"{username}: {message}"
                print(f"Received: {full_message}")
                broadcast(full_message, client_socket)
            else:
                break
        except:
            break

    # Удаляем пользователя из списков при отключении
    broadcast(f"{username} покинул чат.", client_socket)
    del usernames[client_socket]
    del client_sockets[client_socket]
    client_socket.close()


def broadcast(message, client_socket):
    for socket in client_sockets:
        if socket != client_socket:
            socket.send(message.encode())


def start_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} connected.")

        # Создаем новый поток для обработки клиента
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    start_server()