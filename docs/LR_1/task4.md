## Задание №4. Многопользовательский чат

### Описание: 
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

### Требования:
* Обязательно использовать библиотеку socket.
* Для многопользовательского чата необходимо использовать библиотеку threading.

### Реализация:

* Протокол TCP: 100% баллов.
* Протокол UDP: 80% баллов.
* Для UDP используйте threading для получения сообщений на клиенте.
* Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

### Листинг кода:
#### server.py
```
import socket
import threading

clients = {}


def new_client(connection, address):
    print(f"New connection: {address}")
    connection.send("Welcome! Enter your name or nickname: ".encode())
    name = connection.recv(1024).decode()
    clients[connection] = name
    if len(clients.values()) == 1:
        connection.send(f"Hello, {name}!".encode())
    else:
        connection.send(f"Hello, {name}! {', '.join(clients.values())} are in the chat".encode())
    send_to_all(f"{name} is online", connection)
    while True:
        try:
            message = connection.recv(1024).decode()
            if not message:
                break
            send_to_all(f"{name}: {message}", connection)
        except:
            break
    connection.close()
    del clients[connection]
    client_left(name)
    print(f"Closed connection: {address}")


def client_left(name):
    for client in clients:
        try:
            client.send(f"{name} left chat".encode())
        except:
            break


def send_to_all(message, sender_connection):
    for client in clients:
        if client != sender_connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.pop(client)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 1234))
server_socket.listen()
print("Server started")
while True:
    client_connection, client_address = server_socket.accept()
    thread = threading.Thread(target=new_client, args=(client_connection, client_address))
    thread.start()

```

#### client.py
``` 
import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            client_message = client_socket.recv(1024)
            if not client_message:
                break
            print(client_message.decode())
        except:
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(('127.0.0.1', 1234))
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    while True:
        client_message = input()
        if client_message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(client_message.encode())

```

### Пояснение:
При реализации было принято решение сделать многопользовательский чат с применением TCP протокола. У клиента есть возможность отправлять сообщения, видеть всех учатников чата, а также при желании выходить из чата с помощью кодового слова "exit". Если говорить о серверной части, было реализовано запоминание каждого пользователя в словаре (с его подключением и адресом), обработка входящих сообщений и перенаправление остальным клиентам, удаление клиента из чата и информирование об этом остальных, а также запоминание всех входящих и выходящих клиентов путем простого вывода данной информации в консоль. Каждый клиент может видеть, кто сейчас онлайн, кто покинул чат, а кто отправил каждое сообщение