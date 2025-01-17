# Отчет по Заданию 4: Многопользовательский чат

## Описание задания
Реализовать многопользовательский чат с использованием потоков для обработки клиентов.

## Реализация

### Сервер:
```
import socket
import threading

clients = []

def handle_client(client_socket, addr):
    print(f"Подключен клиент: {addr}")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"{addr}: {message}")
                broadcast(message, client_socket)
            else:
                remove(client_socket)
                break
        except:
            remove(client_socket)
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                remove(client)

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 4040))
server_socket.listen(5)

print("Сервер ожидает подключения...")

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
```
### Клиент:
```
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 4040))

# Запуск потока для получения сообщений
threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    message = input()
    if message:
        client_socket.send(message.encode())
```
## Вывод:
Многопользовательский чат с потоками реализован и успешно работает.

