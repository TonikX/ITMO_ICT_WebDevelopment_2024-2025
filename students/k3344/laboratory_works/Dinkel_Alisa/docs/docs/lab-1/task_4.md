# Задание 4

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

- Язык реализации: Python
- Протокол: TCP
- Используемые библиотеки: socket, threading

Реализован многопользовательский чат.

## Реализация
client.py
```python
import socket
import threading


HOST = 'localhost'  # Адрес хоста (localhost для локальных соединений)
PORT = 8082         # Порт, на котором будет работать сервер

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect((HOST, PORT))


# Функция для приема сообщений
def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            print(msg)
        except:
            client_socket.close()
            break


# Запускаем поток для приема сообщений
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Ввод имени
name = input("Введите ваше имя: ")
client_socket.send(name.encode("utf-8"))

# Основной ввод сообщений
while True:
    msg = input()
    if msg.lower() == "exit":
        client_socket.send(msg.encode("utf-8"))
        break
    client_socket.send(msg.encode("utf-8"))

# Закрываем соединение
client_socket.close()
```
server.py
```python
import socket
import threading

# Параметры сервера
HOST = 'localhost'  # Адрес хоста (localhost для локальных соединений)
PORT = 8082         # Порт, на котором будет работать сервер

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие соединения
server_socket.listen(5)
print(f"HTTP сервер запущен на {HOST}:{PORT}...")

clients = {}  # Словарь для хранения клиентов (сокет -> имя)
addresses = {}  # Словарь для хранения адресов клиентов


# Функция для обработки входящих соединений
def accept_incoming_connections():
    while True:
        client, client_address = server_socket.accept()
        print(f"Подключение от {client_address}")
        client.send("Введите имя и нажмите Enter: ".encode("utf-8"))
        addresses[client] = client_address  # Сохраняем адрес клиента
        threading.Thread(target=handle_client, args=(client,)).start()  # Создаем поток для клиента


# Функция обработки сообщений от одного клиента
def handle_client(client, client_address):
    name = client.recv(1024).decode("utf-8")  # Получаем имя клиента
    clients[client] = name  # Добавляем клиента в список

    welcome = f"{name}, добро пожаловать в чат!\nДля выхода напишите 'exit'."
    client.send(welcome.encode("utf-8"))
    msg = f"{name} присоединился к чату!"
    broadcast(msg, sender_client=client)  # Оповещаем всех, кроме нового клиента

    while True:
        msg = client.recv(1024).decode("utf-8")
        if msg.lower() == "exit":
            client.send("Вы покинули чат.".encode("utf-8"))
            client.close()
            del clients[client]  # Удаляем из списка
            broadcast(f"{name} покинул чат.", sender_client=client)  # Оповещаем всех, кроме покидающего чат
            break
        else:
            broadcast(msg, name, sender_client=client)  # Оповещаем всех, кроме отправителя


# Функция для отправки сообщений всем клиентам
def broadcast(msg, name="Сервер", sender_client=None):
    full_msg = f"{name}: {msg}"
    for client in clients:
        # Отправляем сообщение всем, кроме клиента, который его отправил
        if client != sender_client:
            client.send(full_msg.encode("utf-8"))


# Основной цикл сервера для ожидания клиентов
while True:
    client_socket, client_address = server_socket.accept()  # Принимаем новое подключение
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()  # Запускаем обработку клиента в отдельном потоке
```
## Запуск
- Запустите сервер:
```bash
python server.py
```
- Запустите клиента:
```bash
python client.py
```