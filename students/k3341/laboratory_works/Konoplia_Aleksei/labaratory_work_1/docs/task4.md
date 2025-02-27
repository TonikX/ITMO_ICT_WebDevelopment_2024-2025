# Задание 4

## Многопользовательский чат

### Задание

Реализовать многопользовательский чат с использованием потоков для обработки сообщений от разных пользователей.

#### Клиент
``` python 
import socket
import threading

def chat_client():
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                print(message)
            except:
                print("Отключено от сервера")
                client_socket.close()
                break

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 34567))

    threading.Thread(target=receive_messages).start()

    while True:
        message = input()
        client_socket.sendall(message.encode())

if __name__ == '__main__':
    chat_client()
```

#### Сервер
``` python 
import socket
import threading

def chat_server():
    clients = []

    def handle_client(client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    broadcast(message, client_socket)
            except:
                clients.remove(client_socket)
                client_socket.close()
                break

    def broadcast(message, sender_socket):
        for client in clients:
            if client != sender_socket:
                client.sendall(message.encode())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 34567))
    server_socket.listen(5)
    print("Чат сервер запущен на порту 34567")

    while True:
        client_socket, _ = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    chat_server()
```