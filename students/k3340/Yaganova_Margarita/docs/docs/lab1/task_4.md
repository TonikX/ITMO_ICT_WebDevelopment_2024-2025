### Задание 4:

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.
Реализация:
Протокол TCP: 100% баллов.
Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

### Ход работы:

#### server.py

```
import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 8080
ENCODING = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except OSError:  # Handles socket errors
            if client in clients:
                disconnect_client(client)
            break


def disconnect_client(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    nicknames.remove(nickname)
    broadcast(f'{nickname} left!'.encode(ENCODING))


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('margo'.encode(ENCODING))
        nickname = client.recv(1024).decode(ENCODING)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode(ENCODING))
        client.send('Connected to server!'.encode(ENCODING))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == "__main__":
    print(f"Server running on {SERVER_HOST}:{SERVER_PORT}")
    receive()
```


#### client.py

```
import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
ENCODING = 'utf-8'


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode(ENCODING)
            if message == 'margo':
                client_socket.send(nickname.encode(ENCODING))
            else:
                print(message)
        except OSError:
            print("An error occurred while receiving data!")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = f'{nickname}: {input("")}'
        client_socket.send(message.encode(ENCODING))


if __name__ == "__main__":
    nickname = input("Choose your nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionError:
        print("Failed to connect to the server.")
        exit()

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    write_thread = threading.Thread(target=send_messages, args=(client,))
    write_thread.start()
```

TCP соединение обеспечивается созданием TCP-socket с помощью параметра `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`

В серверной части чата после определения соединения прописываем основную функцию работы с 
клиентами: приём сообщений пользователя с условиями. Сначала транслируется присоединение 
пользователя к беседе. Если клиент желает выйти из чата с помощью 
кодового слова, то эта новость распространяется между другими пользователями и клиент удаляется 
из списка участников чата и его связь обрывается. В ином случае, если клиент отправил обычное 
сообщение, то оно транслируется другим участникам чата с именем отправителя.

В клиентской части прописывается получение чужих сообщений и объявлений сервера. При попытке 
выйти из чата связь пользователя с сервером обрывается.
