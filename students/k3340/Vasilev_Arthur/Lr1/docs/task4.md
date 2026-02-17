# Задание 4: Многопользовательский чат

## Описание

Реализован многопользовательский чат-сервер с использованием TCP протокола и потоков для одновременной обработки нескольких клиентов.

## Файлы реализации

- `server.py` - Чат-сервер
- `client.py` - Чат-клиент

## Особенности реализации

- Поддержка нескольких пользователей одновременно
- Использование потоков для обработки подключений
- Автоматическое уведомление о входе/выходе пользователей
- Команды: `/online`, `/quit`
- Потокобезопасная работа с общими данными

## Код сервера

```python
import socket
import threading
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=8084):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {} 
        self.running = True
        self.lock = threading.Lock()  

    def broadcast_message(self, message, sender_socket=None):
        """Отправляет сообщение всем подключенным клиентам, кроме отправителя"""
        with self.lock:
            disconnected_clients = []

            for client_socket, client_info in self.clients.items():
                try:
                    if client_socket != sender_socket:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        formatted_message = f"[{timestamp}] {message}\n"
                        client_socket.send(formatted_message.encode('utf-8'))
                except (BrokenPipeError, ConnectionResetError, OSError):
                    disconnected_clients.append(client_socket)

            for client_socket in disconnected_clients:
                if client_socket in self.clients:
                    username = self.clients[client_socket]['username']
                    print(f"Клиент {username} отключился (ошибка отправки)")
                    del self.clients[client_socket]
                    client_socket.close()

    def handle_client(self, client_socket, client_address):
        """Обрабатывает соединение с одним клиентом"""
        username = None

        try:
            client_socket.send("Введите ваше имя: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()

            if not username:
                username = f"Гость_{client_address[1]}"

            with self.lock:
                self.clients[client_socket] = {
                    'username': username,
                    'address': client_address,
                    'join_time': datetime.now()
                }

            join_message = f">>> {username} присоединился к чату!"
            print(join_message)
            self.broadcast_message(join_message, client_socket)

            welcome_msg = f"\nДобро пожаловать в чат, {username}!\n" \
                         f"Сейчас в чате: {len(self.clients)} пользователь(ей)\n" \
                         f"Команды:\n" \
                         f"/online - список онлайн пользователей\n" \
                         f"/quit - выход из чата\n" \
                         f"="*50 + "\n"
            client_socket.send(welcome_msg.encode('utf-8'))

            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8').strip()

                    if not message:
                        break  

                    if message.startswith('/'):
                        if message == '/quit':
                            break
                        elif message == '/online':
                            online_users = []
                            with self.lock:
                                for info in self.clients.values():
                                    online_users.append(info['username'])
                            response = f"Онлайн пользователи ({len(online_users)}): " + ", ".join(online_users) + "\n"
                            client_socket.send(response.encode('utf-8'))
                        else:
                            client_socket.send("Неизвестная команда. Используйте /help для списка команд.".encode('utf-8'))
                    else:
                        chat_message = f"{username}: {message}"
                        print(f"{datetime.now().strftime('%H:%M:%S')} {chat_message}")
                        self.broadcast_message(chat_message, client_socket)

                except (ConnectionResetError, BrokenPipeError):
                    break
                except UnicodeDecodeError:
                    client_socket.send("Ошибка: неверная кодировка сообщения".encode('utf-8'))

        except Exception as e:
            print(f"Ошибка при работе с клиентом {client_address}: {str(e)}")
        finally:
            if client_socket in self.clients:
                with self.lock:
                    if client_socket in self.clients:
                        username = self.clients[client_socket]['username']
                        del self.clients[client_socket]

                if username:
                    leave_message = f"<<< {username} покинул чат."
                    print(leave_message)
                    self.broadcast_message(leave_message)

            client_socket.close()

    def start(self):
        """Запускает сервер"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"Чат-сервер запущен на {self.host}:{self.port}")
        print("Ожидание подключений...")

        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                print(f"Новое подключение: {client_address}")

                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

        except KeyboardInterrupt:
            print("\nОстановка сервера...")
            self.running = False
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
```

## Код клиента

```python
import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='localhost', port=8084):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = True

    def receive_messages(self):
        """Получает сообщения от сервера в отдельном потоке"""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(message, end='')
                else:
                    break
            except (ConnectionResetError, BrokenPipeError):
                break
            except UnicodeDecodeError:
                print("Ошибка: получено сообщение с неверной кодировкой")

    def start(self):
        """Запускает клиент"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Подключено к серверу {self.host}:{self.port}")

            # Запускаем поток для приема сообщений
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            while self.running:
                try:
                    message = input()
                    if message.lower() in ['/quit', 'exit']:
                        self.running = False
                        break
                    self.client_socket.send(message.encode('utf-8'))
                except KeyboardInterrupt:
                    self.running = False
                    break

        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            self.client_socket.close()
            print("Отключено от сервера")

if __name__ == "__main__":
    client = ChatClient()
    client.start()
```

## Запуск

1. Запустите сервер: `python server.py`
2. Запустите несколько клиентов в разных терминалах: `python client.py`
3. Введите имя пользователя и начинайте общаться