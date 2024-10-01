# Реализация многопользовательского чата

## Условие

**Задача**: Реализовать многопользовательский чат, где клиенты могут подключаться к серверу, отправлять сообщения и получать их от других пользователей. Для реализации требуется использование библиотеки `socket` для сетевых операций и библиотеки `threading` для работы с потоками.

**Требования**:

  1. Многопользовательская поддержка (больше двух пользователей).
  2. Использование потоков для обработки сообщений от разных пользователей.
  3. Отправка сообщений от одного пользователя всем остальным участникам чата.

## Решение

В данной задаче реализован многопользовательский чат с серверной и клиентской частью.

- **Серверная часть** отвечает за обработку подключений пользователей, отправку и получение сообщений, а также за рассылку сообщений другим участникам чата. Сервер управляет потоками для каждого пользователя и сохраняет информацию о подключённых клиентах.
- **Клиентская часть** позволяет пользователям подключаться к серверу, отправлять и получать сообщения.

### Возможности:

1. **Использование библиотеки `socket`**: Все взаимодействие между сервером и клиентами осуществляется с помощью TCP-сокетов, которые позволяют отправлять и получать сообщения в текстовом формате.
2. **Использование `threading`**: Каждое клиентское соединение на стороне сервера обрабатывается в отдельном потоке, что позволяет обрабатывать сообщения от нескольких клиентов параллельно.
3. **Многопользовательский режим**: Сервер поддерживает подключение и взаимодействие между несколькими пользователями одновременно. Все подключенные пользователи сохраняются в словаре `users`, где ключом является имя пользователя, а значением — сокет клиента.
4. **Персональные сообщения**: Пользователи могут отправлять приватные сообщения другим пользователям, добавив символ `@` перед именем целевого пользователя.

### Описание работы функций

1. **Функция `broadcast`**:

> Отвечает за отправку сообщений всем пользователям, за исключением отправителя.
> Если сообщение отправляется конкретному пользователю, то проверяется наличие этого пользователя в системе, и если он подключен, сообщение доставляется только ему.

2. **Функция `handle_client`**:

> Управляет взаимодействием с клиентом. После подключения клиента, запрашивается его имя, которое используется для идентификации в чате.
> Функция обрабатывает все входящие сообщения клиента и передает их через `broadcast` другим пользователям.
> Также поддерживает отправку персональных сообщений через символ `@`.

3. **Функция `start_server`**:

> Основная функция сервера, которая ожидает подключения клиентов и запускает отдельный поток для каждого нового клиента с помощью `threading.Thread`.

4. **Функция `receive_messages` (на стороне клиента)**:

> Поток на стороне клиента, который принимает входящие сообщения от сервера и выводит их на экран.

5. **Функция `start_client`**:

> Основная функция клиента, которая подключается к серверу и запускает поток для приема сообщений, одновременно позволяя пользователю вводить свои собственные сообщения.

### Пример работы чата

1. **Подключение клиента**:

> Клиент подключается к серверу и вводит свое имя. Если имя уже занято, подключение прерывается.
> Если имя уникально, клиент присоединяется к чату, и всем другим пользователям отправляется сообщение о новом участнике.

2. **Отправка сообщений**:

> Клиент может отправлять обычные сообщения, которые видят все участники чата, или персональные сообщения, указав `@user_name` в начале сообщения.

3. **Отключение клиента**:

> Если клиент закрывает соединение или происходит ошибка, сервер отключает его и уведомляет остальных участников чата.

## Код

`server.py`

```python
import socket
import threading

green_s = '\033[32m'
red_s = '\033[31m'
green_e = '\033[0m'
red_e = '\033[0m'
users = {}


def broadcast(message, sender_socket=None, target_user=None):
    if target_user:
        target_socket = users.get(target_user)
        if target_socket:
            try:
                target_socket.send(message)
            except:
                target_socket.close()
                del users[target_user]
                print(f"{red_s}Ошибка при отправке сообщения пользователю {target_user}{red_e}")
        else:
            print(f"{red_s}Пользователь {target_user} не найден{red_e}")
            sender_socket.send(f"{red_s}Ошибка: Пользователь {target_user} не найден{red_e}".encode('utf-8'))
        return

    for user, client_socket in users.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del users[user]


def handle_client(client_socket, client_address):
    print(f"Новое подключение: {client_address}")

    client_socket.send("Введите своё имя: ".encode('utf-8'))
    user_name = client_socket.recv(1024).decode('utf-8')
    if user_name in users:
        client_socket.send("Имя уже занято, подключение прервано.\n".encode('utf-8'))
        client_socket.close()
        return
    users[user_name] = client_socket

    broadcast(f"{green_s}{user_name} присоединился к чату.{green_e}".encode('utf-8'), client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"{user_name}: {message.decode('utf-8')}")

            if message.decode('utf-8').startswith("@"):
                target_user, personal_message = message.decode('utf-8').split(' ', 1)
                target_user = target_user[1:]
                broadcast(
                    f"{user_name} {green_s}(лично для {target_user}){green_e}: {personal_message}".encode('utf-8'),
                    client_socket, target_user=target_user)
            else:
                broadcast(f"{user_name}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
        except:
            client_socket.close()
            del users[user_name]
            broadcast(f"{red_s}{user_name} покинул чат.{red_e}".encode('utf-8'))
            break


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 1234))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


start_server()
```

`client*.py`

```python
import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("Ошибка")
            client_socket.close()
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1234))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()


start_client()
```
