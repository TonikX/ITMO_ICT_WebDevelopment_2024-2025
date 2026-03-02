# Задание
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте 
многопользовательский чат.

**Требования:**

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.
- Протокол TCP: 100% баллов.
- Протокол UDP: 80% баллов.
- Для UDP используйте threading для получения сообщений на клиенте.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять
пользователей, чтобы отправлять им сообщения.
 
***

# Решение

## Клиент

```python
import socket
import threading

HOST = 'localhost'
PORT = 9090

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'nickname':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Disconnected from server.")
            client.close()
            break


def write_message():
    while True:
        text = input()

        if text == "/quit":
            client.send(f"{nickname} left the chat.".encode('utf-8'))
            client.close()
            break
        else:
            message = f"{nickname}: {text}"
            client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()

```

## Сервер

```python
import socket
import threading

HOST = 'localhost'
PORT = 9090

clients = []     # список сокетов клиентов
nicknames = []   # список никнеймов


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()

                nickname = nicknames[index]
                nicknames.remove(nickname)

                broadcast(f"{nickname} left the chat.".encode('utf-8'))
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Server started, waiting for connections...")

    while True:
        client, address = server.accept()
        print(f"Connected: {address}")

        client.send('nickname'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        clients.append(client)
        nicknames.append(nickname)

        print(f"Client nickname: {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("You are connected to the chat!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()

```

***

# Пояснение

# Простой чат-сервер на Python

Данный код реализует многопользовательский чат-сервер, работающий по локальной сети.

## Принцип работы

1. Сервер запускается и ожидает подключения клиентов
2. При подключении новый клиент получает запрос на ввод ника
3. Сервер сохраняет клиента и его ник в общие списки
4. Все сообщения от одного клиента автоматически рассылаются всем остальным
5. При отключении клиента остальные участники получают уведомление

## Основные компоненты

- **`broadcast(message)`** — отправляет полученное сообщение всем подключённым клиентам
- **`handle_client(client)`** — обрабатывает сообщения конкретного клиента в отдельном потоке
- **`main()`** — главный цикл сервера, принимает новые подключения и создаёт потоки

## Особенности реализации

- Каждый клиент работает в отдельном потоке (`threading`)
- Сервер может обслуживать несколько клиентов одновременно
- Используется сокет TCP (`socket.SOCK_STREAM`)
- При отключении клиента автоматически удаляет его из списков и оповещает других

## Технические детали

- **Хост:** `127.0.0.1` (локальный)
- **Порт:** `9090`
- **Максимальная очередь подключений:** 5
- **Размер буфера:** 1024 байта