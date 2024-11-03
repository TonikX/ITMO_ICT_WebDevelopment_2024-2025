### Задание

Реализовать многопользовательский чат с использованием TCP, socket, threading.

### `server.py`

```python
import socket
import threading

clients = []


def broadcast(message, client_socket):
    for client in clients:
        if client['socket'] != client_socket:
            try:
                client['socket'].send(message)
            except:
                clients.remove(client)


def handle_client(client_socket):
    try:
        name = client_socket.recv(1024).decode('utf-8')
        clients.append({"socket": client_socket, "name": name})

        welcome_message = f"{name} присоединился к чату!".encode('utf-8')
        broadcast(welcome_message, client_socket)
        print(welcome_message.decode('utf-8'))

        while True:
            message = client_socket.recv(1024)
            dec_message = message.decode('utf-8')
            if dec_message != "leave":
                formatted_message = f"{name}: {dec_message}".encode('utf-8')
                print(formatted_message.decode('utf-8'))
                broadcast(formatted_message, client_socket)
            else:
                break
    finally:
        print(f"{name} отключился.")
        clients.remove({"socket": client_socket, "name": name})
        broadcast(f"{name} покинул чат.".encode('utf-8'), client_socket)
        client_socket.close()


def start_server(host='127.0.0.1', port=5555):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[СЕРВЕР ЗАПУЩЕН] Ожидание подключений на {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ] {client_address} подключился.")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
```

### `client.py`

```python
import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("Произошла ошибка при получении сообщения.")
            client_socket.close()
            break


def send_messages(client_socket):
    while True:
        message = input("")
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            print("Произошла ошибка при отправке сообщения.")
            client_socket.close()
            break


def start_client(host='127.0.0.1', port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    name = input("Введите ваше имя: ")
    client_socket.send(name.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


if __name__ == "__main__":
    start_client()
```

Сервер создает сокет с TCP-подключением и ожидает подключений. Клиент подключается к хосту и вводит свое имя. Для каждого клиента запускается поток на отправление и получение сообщений. Сообщения клиента логируются на сервере и отправляются остальным пользователям. При вводе команды "leave" сокет клиента закрывается.