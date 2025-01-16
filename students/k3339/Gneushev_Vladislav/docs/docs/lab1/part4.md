## Задание

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

## Решение

Был реализован многопользовательский чат при помощи протокола TCP. В чате есть возможность ввода имени. Каждый человек видит сообщения, присылаемые другими пользователями.


## Как запустить

Клиент: Зайти в папку `lab1/part4` и запустить командой `python client.py`

Сервер: Зайти в папку `lab1/part4/server` и запустить командой `python main.py`

## Код
### Код клиента

```
import socket
import threading
from contextlib import contextmanager

from server.constants import SERVER_HOST, SERVER_PORT


@contextmanager
def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    try:
        yield sock
    finally:
        sock.close()


def send_message(sock, message: str):
    sock.send(message.encode("utf-8"))


def handle_message(sock):
    while True:
        data = sock.recv(1024)
        print(data.decode("utf-8"))


def main():
    with client() as c:
        threading.Thread(target=handle_message, args=(c,)).start()
        while True:
            message = input()
            send_message(c, message)


if __name__ == "__main__":
    main()
```


### Код сервера

Для сервера реализованы сущности: Менеджер соединений (`ConnectionManager`), Сервер (`Server`)

#### Менеджер соединений (`ConnectionManager`)

```
class ConnectionManager:
    def __init__(self):
        self.connections: list[Connection] = []

    def add_connection(self, connection: Connection):
        # connection.set_timeout(1.0)
        self.connections.append(connection)

    def broadcast_message(
            self,
            message: str,
            exclude_nonames: bool = False
    ):
        for connection in self.connections:
            if exclude_nonames and connection.user_name is None:
                continue
            connection.send_message(message)

    def close_all_connections(self):
        for connection in self.connections:
            connection.close()
        self.connections.clear()

    def remove_connection(self, connection: Connection):
        if connection in self.connections:
            self.connections.remove(connection)
```


#### Сервер (`Server`)

```
class Server:
    def __init__(
            self,
            host: str,
            port: int,
            connection_manager: ConnectionManager,
    ):
        self.host = host
        self.port = port
        self.connection_manager = connection_manager
        self.server_socket = socket(AF_INET, SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        logger.info(f"Server started on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            connection = Connection(sock=conn, address=addr)
            self.connection_manager.add_connection(connection)
            logger.info(f"Accepted connection from {addr}")

            threading.Thread(target=self._handle_client, args=(connection,)).start()

    def _handle_client(self, connection: Connection):
        with connection.sock:
            while True:
                try:
                    message = connection.receive_message()
                    if message is None:
                        break
                    self._handle_message(message, connection)
                except Exception as e:
                    self.connection_manager.remove_connection(connection)

    def _handle_message(self, message: str, connection: Connection):
        if connection.user_name is None:
            connection.user_name = message
            logger.info(f"connection [{connection}]: set username - {message}")
            return

        logger.info(f"Received message: {message} from {connection}")
        self.connection_manager.broadcast_message(
            f"[{connection.user_name}]: {message}",
            exclude_nonames=True
        )

    def stop(self):
        self.connection_manager.close_all_connections()
        self.server_socket.close()
        logger.info("Server stopped")

```