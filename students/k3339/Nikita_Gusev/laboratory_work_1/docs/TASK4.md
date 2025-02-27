# Задание №4

## Текст задания

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:

Обязательно использовать библиотеку socket.
Для многопользовательского чата необходимо использовать библиотеку threading.
Реализация:

Протокол TCP: 100% баллов.
Протокол UDP: 80% баллов.
Для UDP используйте threading для получения сообщений на клиенте.
Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

Я сделала многопользовательский чат, используя протокол TCP.

## UDP Сервер

Этот код реализует многопользовательский чат-сервер на Python, использующий TCP-сокеты. Сервер принимает соединения от клиентов, запрашивает у них имя, добавляет их в список пользователей и рассылает сообщения всем подключенным клиентам. Функция `handle_client` обрабатывает каждое соединение в отдельном потоке, что позволяет одновременно обслуживать нескольких клиентов. При получении сообщения от клиента оно транслируется всем остальным участникам чата, а при отключении клиента сервер удаляет его из списка и уведомляет остальных. Сервер настраивается на прослушивание заданного адреса и порта.

```python
import socket
import threading

# Настройки сервера
HOST = 'localhost'
PORT = 8080

# Список клиентов
clients = []
usernames = []

# Функция для обработки сообщений от клиентов
def handle_client(client_socket, address):
    print(f"{address} подключился.")
    client_socket.send("Введите ваше имя:".encode())
    username = client_socket.recv(1024).decode()
    usernames.append(username)
    clients.append(client_socket)

    broadcast(f"{username} присоединился к чату.".encode(), client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(f"{username}: {message.decode()}".encode(), client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue

# Функция для рассылки сообщений всем клиентам
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

# Функция для удаления клиента из списков
def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        username = usernames[index]
        usernames.remove(username)
        broadcast(f"{username} покинул чат.".encode(), client_socket)

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Сервер запущен...")

# Запуск обработки клиентов
while True:
    client_socket, address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, address)).start()

```

## UDP Клиент

Этот код реализует TCP-клиент на Python для подключения к чат-серверу. Клиент настраивает сокет и соединяется с сервером, после чего запускает отдельный поток для получения сообщений. Пользователь вводит свое имя, которое отправляется на сервер. Затем клиент входит в основной цикл, где он может отправлять сообщения на сервер. Если пользователь вводит "выход", соединение закрывается. Код обрабатывает ошибки при получении сообщений и закрывает сокет в случае возникновения проблем.

```python
import socket
import threading

# Настройки клиента
HOST = 'localhost'
PORT = 8080

# Функция для получения сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Ошибка при получении сообщения.")
            client_socket.close()
            break

# Настройка клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Запуск потока для получения сообщений
threading.Thread(target=receive_messages, args=(client_socket,)).start()

# Ввод имени пользователя
username = input("Введите ваше имя: ")
client_socket.send(username.encode())

# Основной цикл для отправки сообщений
while True:
    message = input()
    if message.lower() == 'выход':
        break
    client_socket.send(message.encode())

client_socket.close()

```

