# Задание 4:

## Описание задания
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

## Требования:
- Обязательно использовать библиотеку `socket` для создания TCP-соединений.
- Для многопользовательского чата необходимо использовать библиотеку threading.

## Реализация:
- Протокол TCP: 100% баллов.
- Протокол UDP: 80% баллов.
- Для UDP используйте `threading` для получения сообщений на клиенте.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

### Серверная часть:
Сервер принимает подключения от нескольких клиентов, создавая отдельный поток для обработки каждого нового клиента. Все сообщения, которые отправляют клиенты, передаются другим пользователям чата.

```python
import socket
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = sock.accept()
        print(f"Подключился новый пользователь с адресом {client_address}.")
        message = "Введите своё имя"
        client.send(message.encode())
        client_name = client.recv(1024).decode()
        clients[client_name] = client
        Thread(target=handle_client, args=(client, client_name)).start()


def handle_client(client, client_name):
    welcome_message = f"{client_name}, Добро пожаловать в чат"
    client.send(welcome_message.encode())
    message_other_clients = f"Внимание! В чат зашел новый пользователь с именем {client_name}"
    broadcast(message_other_clients, client_name)

    while True:
        try:
            message = client.recv(1024).decode()
            print(f"{client_name}: {message}")
            if message.lower() == "exit":
                goodbye_message = f"{client_name} покинул чат"
                broadcast(goodbye_message, client_name)
                client.close()
                del clients[client_name]
                break
            else:
                broadcast(f"{client_name}: {message}", client_name)
        except:
            print(f"Ошибка с клиентом {client_name}: {e}")
            goodbye_message = f"{client_name} покинул чат"
            broadcast(goodbye_message, client_name)
            client.close()
            del clients[client_name]
            break


def broadcast(msg, sender_name):
    if clients:
        for client_name, client_socket in clients.items():
            if client_name != sender_name:
                client_socket.sendall(msg.encode())


clients = {}

HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
print("Ждем подключений")
accept_thread = Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()
sock.close()
```

### Клиентская часть:
Клиент подключается к серверу, получает и отправляет сообщения. Для получения сообщений от других участников чата и отправки своих сообщений используются отдельные потоки.

```python
import socket
from threading import Thread

HOST = 'localhost'
PORT = 8080

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((HOST, PORT))


def receive():
    while True:
        try:
            message = client_sock.recv(1024).decode()
            if message:
                print(message)
            else:
                print("Сервер закрыл соединение")
                break
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            break

def send():
    while True:
        message = input()
        client_sock.send(message.encode())
        if message.lower() == "exit":
            print("Выход из чата")
            client_sock.close()
            break


receive_thread = Thread(target=receive)
receive_thread.start()

send_thread = Thread(target=send)
send_thread.start()

receive_thread.join()
send_thread.join()
```

