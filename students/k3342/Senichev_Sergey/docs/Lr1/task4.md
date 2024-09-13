# Задание 4: Чат-сервер

Реализовать двухпользовательский или **многопользовательский** чат. Для максимального количества баллов реализуйте многопользовательский чат.  

Требования:  
- Обязательно использовать библиотеку `socket`.
- Для многопользовательского чата необходимо использовать библиотеку `threading`.

Реализована многопользовательская версия задания. Пользователи могут одновременно находиться в чате. При общении также видно имя пользователя, отправившего сообщение. Реализованы уведомления о входе и выходе пользователя из чата. 

## Файлы
- `chat_server.py`: Реализация сервера
```python
import socket
import threading

buffer_size = 1024
host = 'localhost'
port = 8000
server_address = (host, port)

clients = []
client_names = {}

def handle_client(client_socket):
    client_socket.send("Enter your username: ".encode('utf-8'))
    client_name = client_socket.recv(buffer_size).decode('utf-8')
    client_names[client_socket] = client_name
    broadcast(f"{client_name} joined the chat".encode('utf-8'), client_socket)

    while True:
        try:
            message = client_socket.recv(buffer_size)
            if message:
                broadcast(f"{client_name}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                remove_client(client)


def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_name = client_names[client_socket]
        broadcast(f"{client_name} left the chat".encode('utf-8'), client_socket)
        del client_names[client_socket]


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print(f"Server is running on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connection: {client_address}")

        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    server()
```

- `chat_client.py`: Реализация TCP клиента
```python
import socket
import threading

buffer_size = 1024
host = 'localhost'
port = 8000
server_address = (host, port)

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(buffer_size).decode()
            if message:
                print(f"\n{message}")
        except:
            print("Error while connecting to server.")
            client_socket.close()
            break

def server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.send(message.encode())

if __name__ == "__main__":
    server()
```
