# Задание 4: Многопользовательский чат

## Краткое описание задания

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

## Стек реализации

- Язык: Python
- Библиотеки: socket, threading
- Протокол: TCP

## Как запускать

* Запустите сервер:

```bash
python server.py
```

* Запустите несколько клиентов в разных терминалах:

```bash
python client.py
```

## Листинг кода

### client.py

```python
import socket
import threading


def receive_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except (Exception, KeyboardInterrupt):
            client_socket.close()
            break


def send_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            message = input().strip()
            client_socket.send(message.encode())
        except (Exception, KeyboardInterrupt):
            client_socket.close()
            break

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 12345))

    send_thread = threading.Thread(target=send_messages, args=(conn,))
    receive_thread = threading.Thread(target=receive_messages, args=(conn,))

    send_thread.start()
    receive_thread.start()

    try:
        receive_thread.join()
        send_thread.join()
    except KeyboardInterrupt:
        print("Соединение разорвано")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
```

### server.py

```python
import socket
import threading


class ChatServer:
    def __init__(self, host: str, port: int, max_clients: int = 10):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.bind((host, port))
        self._conn.listen(max_clients)
        self._conn.settimeout(1)

        self._is_running = True
        self._lock = threading.Lock()
        self._clients = []

    def _broadcast(self, message: str, sender_client: socket.socket) -> None:
        for client in self._clients:
            if client == sender_client:
                continue

            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Не получилось отправить сообщение клиенту {client.getpeername()}: {e}")

    def _handle_client(self, client_socket: socket.socket) -> None:
        with self._lock:
            self._clients.append(client_socket)
        
        client_name = client_socket.getpeername()
        message = f"Клиент {client_name} подключился"
        
        self._broadcast(message=message, sender_client=client_socket )
        print(message)

        while self._is_running:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break

                print(f"Получено сообщение от {client_name}: {message}")

                self._broadcast(
                    message=f"{client_name}: {message}",
                    sender_client=client_socket,
                )
            except Exception as e:
                print(f"Ошибка при работе с клиентом {client_name}: {e}")
                break

        self._remove_client(client_socket)

    def _remove_client(self, client_socket: socket.socket):
        with self._lock:
            if client_socket in self._clients:
                self._clients.remove(client_socket)

                message = f"{client_socket.getpeername()} покинул чат"
                self._broadcast(message=message, sender_client=client_socket)
                print(message)

                client_socket.close()

    def _shutdown(self):
        self._is_running = False

        for client in self._clients:
            try:
                client.send("Сервер завершил работу".encode())
                client.close()
            except Exception as e:
                print(f"Ошибка во время отключения клиента: {e}")

        self._conn.close()
        print("Сервер успешно остановлен")

    def serve(self):
        while self._is_running:
            try:
                client_socket, _ = self._conn.accept()
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
                client_thread.start()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                self._shutdown()
                break

def main():
    chat_server = ChatServer(host="localhost", port=12345)
    try:
        chat_server.serve()
    except KeyboardInterrupt:
        print("Сервер остановлен")


if __name__ == "__main__":
    main()

```
