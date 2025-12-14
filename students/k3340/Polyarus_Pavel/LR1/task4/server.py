import socket
import threading


clients = {}
lock = threading.Lock()

HOST = "localhost"
PORT = 8080


def broadcast(msg):
    with lock:
        for client in clients.keys():
            try:
                client.send(msg)
            except:
                pass


def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if msg:
                broadcast(msg)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break


def remove_client(client):
    with lock:
        if client in clients.keys():
            nickname = clients[client]
            del clients[client]
            broadcast(f"[СИСТЕМА]: Пользователь {nickname} покинул(а) чат".encode())
            client.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[СЕРВЕР] Сервер запущен на {HOST}:{PORT} и ожидает подключений...")

    while True:
        client, addr = server_socket.accept()
        print(f'[СЕРВЕР] Подключение от {addr}')

        client.send('NICKNAME'.encode())
        nickname = client.recv(1024).decode()

        with lock:
            clients[client] = nickname

        broadcast(f"[СИСТЕМА]: Пользователь {nickname} присоеденился(ась) к чату".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()



