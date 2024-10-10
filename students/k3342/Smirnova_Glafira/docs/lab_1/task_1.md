### Задание

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### `server.py`

```python
import socket

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 12123)
    server_socket.bind(server_address)

    print("Server is running...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"Received a message: {data.decode('utf-8')}")

        server_socket.sendto(b"Hello, client", client_address)


if __name__ == "__main__":
    udp_server()
```

### `client.py`

```python
import socket

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 12123)
    print("Press Enter to start!")

    try:
        while True:
            s = input()
            if s == "exit":
                break

            message = b"Hello, server"

            print(f"Sending message: {message.decode('utf-8')}")

            client_socket.sendto(message, server_address)

            response, _ = client_socket.recvfrom(1024)
            print(f"Server's response: {response.decode('utf-8')}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    udp_client()
```

Сервер создает сокет, работающий по протоколу UDP и ожидает сообщение от клиента. Клиент аналогично создает сокет, отправляет на адрес сервера сообщение и ожидает ответа. Сообщения клиента отправляются вводом Enter с клавиатуры, при вводе exit сокет клиента закрывается.