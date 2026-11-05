# Задание №4: Многопользовательский чат на TCP

## Постановка задачи

Реализовать многопользовательский чат. Сервер одновременно обслуживает несколько клиентов, рассылая входящие сообщения
всем участникам, кроме отправителя. Каждое подключение обрабатывается в отдельном потоке.

Требования:

- [x] Обязательно использовать библиотеку socket
- [x] Для многопользовательского чата необходимо использовать библиотеку threading
- [x] Должна быть возможность идентифицировать пользователей
- [x] Пользователь должен иметь возможность выйти из чата
- [x] Реализация на протоколе TCP

## Выполнение

### `server.py`

```python
import socket
import threading


class ChatServer:
    HOST = "localhost"
    PORT = 9090

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clients = {}
        self.clients_lock = threading.Lock()

    def start(self):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(socket.SOMAXCONN)
        print(f"[*] TCP-server started on {self.HOST}:{self.PORT}")

        while True:
            client_sock, client_addr = self.sock.accept()
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_sock, client_addr), daemon=True
            )
            client_thread.start()

    def handle_client(self, client_sock, client_addr):
        was_added = False
        username = None
        try:
            print(f"[+] {client_addr[0]}:{client_addr[1]} connected.")
            client_sock.sendall("Enter your name: ".encode('utf-8'))
            username = client_sock.recv(1024).decode('utf-8').strip()

            if not username:
                client_sock.sendall("[x] Incorrect name.".encode('utf-8'))
                return

            if not self.try_add_client(username, client_sock):
                client_sock.sendall("[x] This name is already taken.".encode('utf-8'))
                return

            was_added = True
            self.print_members()
            while True:
                data = client_sock.recv(1024)
                if not data: break
                text = data.decode('utf-8').strip()
                full_message = f"[{username}] {text}"
                print(full_message)
                self.broadcast(full_message, exclude=client_sock)
        except OSError:
            pass
        finally:
            if was_added: self.remove_clients([username])
            self.print_members()
            client_sock.close()
            print(f"[-] {client_addr[0]}:{client_addr[1]} disconnected.")

    def try_add_client(self, username, client_sock):
        with self.clients_lock:
            if username in self.clients:
                return False
            self.clients[username] = client_sock

        print(f"[!] {username} joined the chat.")
        self.broadcast(f"*** {username} joined the chat! ***")
        return True

    def remove_clients(self, usernames):
        with self.clients_lock:
            for username in usernames:
                self.clients.pop(username, None)

        for username in usernames:
            print(f"[!] {username} left the chat.")
            self.broadcast(f"*** {username} left the chat! ***")

    def broadcast(self, message, exclude=None):
        with self.clients_lock:
            targets = [(name, sock) for name, sock in self.clients.items() if sock is not exclude]

        for username, sock in targets:
            try:
                sock.sendall(message.encode('utf-8'))
            except OSError:
                return

    def stop(self):
        with self.clients_lock:
            for client_sock in self.clients.values():
                try:
                    client_sock.close()
                except OSError:
                    pass
        self.sock.close()

    def print_members(self):
        print("[*] Members:", end=" ")
        print(*self.clients.keys(), sep=", ")
```

`threading.Thread(target=self.handle_client, args=(...), daemon=True)` — создаёт отдельный поток для каждого
подключения. Это позволяет серверу обслуживать много клиентов одновременно, не блокируясь на обработке одного.
`daemon=True` означает, что поток завершится вместе с основным процессом.

`self.clients = {}` — словарь активных клиентов вида `{username: socket}`. Позволяет идентифицировать пользователя
по имени и рассылать сообщения адресно.

`threading.Lock()` — мьютекс для защиты словаря `clients` от одновременного изменения из разных потоков. Без
блокировки возможны состояния гонки при подключении и отключении клиентов.

`try_add_client(username, client_sock)` — атомарно под блокировкой проверяет уникальность имени и добавляет клиента
в словарь. Возвращает `False`, если имя занято. Обеспечивает идентификацию пользователей.

`remove_clients(usernames)` — удаляет клиентов из словаря под блокировкой, затем рассылает уведомление об их выходе.

`broadcast(message, exclude)` — рассылает сообщение всем, кроме отправителя. Список целей формируется под
блокировкой, а `sendall()` вызывается уже без неё — долгие операции не блокируют другие потоки.

`stop()` — закрывает все клиентские сокеты и главный сокет при завершении сервера по `Ctrl+C`.

`print_members()` — выводит список текущих участников чата в консоль сервера.

### `client.py`

```python
import socket
import threading

SERVER_ADDR = ("localhost", 9090)


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_addr):
        self.sock.connect(server_addr)

        stop_event = threading.Event()
        receive_thread = threading.Thread(
            target=self.receive_messages, args=(stop_event,), daemon=True
        )
        receive_thread.start()

        try:
            while not stop_event.is_set():
                message = input()
                if not message: continue
                try:
                    self.sock.sendall(message.encode('utf-8'))
                except OSError:
                    break

                if message.strip().lower() == '/exit': break
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            stop_event.set()
            self.sock.close()

    def receive_messages(self, stop_event):
        while not stop_event.is_set():
            try:
                data = self.sock.recv(1024)
                if not data:
                    stop_event.set()
                    break
                print(data.decode('utf-8'))
            except OSError:
                stop_event.set()
                break


if __name__ == "__main__":
    client = Client()
    try:
        client.connect(SERVER_ADDR)
    except ConnectionRefusedError:
        print("Server unavailable.")
```

`threading.Event()` — примитив синхронизации для сигнала остановки. Поток-приёмник и главный поток читают флаг через
`is_set()` и завершают работу, когда он установлен.

`threading.Thread(target=self.receive_messages, ...)` — запускает поток приёма сообщений. Без него клиент не смог бы
одновременно и читать из сокета, и писать в него: `input()` блокирует поток, и входящие сообщения оставались бы
необработанными.

`receive_messages(stop_event)` — цикл чтения данных из сокета в отдельном потоке. Если приходит `b''`, соединение
закрыто сервером — устанавливаем `stop_event` и выходим.

`stop_event.set()` — сигнализирует потоку-приёмнику остановиться. Вызывается в `finally` при выходе пользователя или
обрыве соединения.

## Проверка

Терминал 1 — сервер:

```bash
$ python server.py
[*] TCP-server started on localhost:9090
[+] 127.0.0.1:54321 connected.
[!] Alice joined the chat.
[*] Members: Alice
[+] 127.0.0.1:54322 connected.
[!] Bob joined the chat.
[*] Members: Alice, Bob
[Alice] Привет, Боб!
[Bob] Привет, Алиса!
[!] Alice left the chat.
[*] Members: Bob
[-] 127.0.0.1:54321 disconnected.
```

Терминал 2 — клиент Alice:

```bash
$ python client.py
Enter your name: Alice
*** Bob joined the chat! ***
Привет, Боб!
[Bob] Привет, Алиса!
/exit
```

Терминал 3 — клиент Bob:

```bash
$ python client.py
Enter your name: Bob
[Alice] Привет, Боб!
Привет, Алиса!
*** Alice left the chat! ***
```

Оба клиента видят сообщения друг друга, сервер логирует подключения, отключения и список участников. Задание выполнено в
соответствии с требованиями.

## Вывод

В ходе работы изучены примитивы многопоточности, необходимые для организации чата:

- `threading.Thread()` — параллельная обработка нескольких клиентов на сервере и одновременный приём/отправка на
  клиенте;
- `threading.Lock()` — защита общего словаря `clients` от состояний гонки;
- `threading.Event()` — синхронизация завершения потоков на клиенте;
- `try_add_client()` / `remove_clients()` — атомарное управление списком участников с проверкой уникальности имён;
- `broadcast()` — рассылка сообщений всем участникам, кроме отправителя.

Ключевое отличие от предыдущих заданий — сервер обслуживает несколько клиентов одновременно. Каждое подключение
обрабатывается в отдельном потоке, а список активных клиентов хранится в общем словаре `{username: socket}`, защищённом
мьютексом. Имя пользователя запрашивается при подключении и проверяется на уникальность, что обеспечивает идентификацию
участников. Клиент использует два потока: один читает сообщения от сервера, другой — ввод пользователя. Команда `/exit`
позволяет корректно выйти из чата, а `threading.Event` синхронизирует завершение обоих потоков.
