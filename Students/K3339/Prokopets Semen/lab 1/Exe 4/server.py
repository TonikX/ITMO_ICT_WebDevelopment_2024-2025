import socket
import threading

# Настройки сервера
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"
client_sockets = set()


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Received: {message}")
                # Рассылка сообщения всем клиентам
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    # Удаление клиента из списка при отключении
    client_sockets.remove(client_socket)
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
        client_sockets.add(client_socket)

        # Запуск нового потока для обработки клиента
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    start_server()