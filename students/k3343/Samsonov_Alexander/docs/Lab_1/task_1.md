# Задание 1

## Текст задачи

Реализовать клиентскую и серверную часть приложения. Клиент отсылает серверу
сообщение «Hello, server». Сообщение должно отразиться на стороне сервера.
Сервер в ответ отсылает клиенту сообщение «Hello, client». Сообщение должно
отобразиться у клиента.

- Обязательно использовать библиотеку **socket**
- Реализовать с помощью протокола UDP

## Листинг кода

### Сервер

```python
from datetime import datetime  # for logging
from socket import socket, AF_INET, SOCK_DGRAM


def udp_server(server_address: tuple[str, int] = ('localhost', 12345)):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(server_address)
    # set up the socket

    print(f"Server is up and listening on {server_address}")

    while True:
        try:
            # main loop
            message, client_address = server_socket.recvfrom(1024)
            print(f"Received message from {client_address} at {datetime.now().time()}: {message.decode()}")

            response = b"Hello client!\n"
            server_socket.sendto(response, client_address)
        except KeyboardInterrupt:
            server_socket.close()
            break


if __name__ == "__main__":
    udp_server()

```

### Клиент

```python
from socket import socket, AF_INET, SOCK_DGRAM


def udp_client(server_address: tuple[str, int] = ('localhost', 12345)):
    client_socket = socket(AF_INET, SOCK_DGRAM)

    try:
        # 1 try without validation
        message = b"Hello server\n"
        print(f"Sending: {message}")
        client_socket.sendto(message, server_address)

        response, _ = client_socket.recvfrom(1024)
        print(f"Received: {response.decode()}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    udp_client()

```

## Детализация

Для использования UDP при конфигурации socket используется SOCK_DGRAM.
UDP не требует никакого рукопожатия, достаточно просто отправить пакеты