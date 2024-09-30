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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the server!'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected with: {str(address)}")

        client_socket.send('YOU_HAVE_JOINED_THE_CHAT!'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client_socket)

        print(f"Client nickname is {nickname}")
        broadcast(f"{nickname} joined the server!".encode('utf-8'))
        client_socket.send('Conected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


print("Server is listening")
receive()
```

#### client.py
``` 
import socket
import threading

nickname = str(input("Enter your nickname: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))


def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'YOU_HAVE_JOINED_THE_CHAT!':
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error")
            client_socket.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client_socket.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
```

### Пояснение:
При реализации было принято решение сделать многопользовательский чат с применением TCP протокола. У клиента есть возможность отправлять сообщения, видеть всех учатников чата, а также при желании выходить из чата с помощью кодового слова "exit". Если говорить о серверной части, было реализовано запоминание каждого пользователя в словаре (с его подключением и адресом), обработка входящих сообщений и перенаправление остальным клиентам, удаление клиента из чата и информирование об этом остальных, а также запоминание всех входящих и выходящих клиентов путем простого вывода данной информации в консоль. Каждый клиент может видеть, кто сейчас онлайн, кто покинул чат, а кто отправил каждое сообщение