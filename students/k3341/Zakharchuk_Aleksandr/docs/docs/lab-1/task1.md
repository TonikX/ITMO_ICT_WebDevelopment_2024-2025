# Задание 1: UDP Клиент-Сервер

## Краткое описание задания

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», которое должно отображаться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое отображается у клиента.

## Стек реализации

- Язык: Python
- Библиотека: socket
- Протокол: UDP

## Как запускать

* Запустите сервер:

```bash
python server.py
```

* Запустите клиента:

```bash
python client.py
```

## Листинг кода

### client.py

```python
import socket


def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.connect(("localhost", 12345))

    conn.send("Hello, server".encode())

    data = conn.recv(1024)
    print(data.decode())

    conn.close()


if __name__ == "__main__":
    main()
```

### server.py

```python
import socket

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.bind(("localhost", 12345))

    data, address = conn.recvfrom(1024)
    print(data.decode())

    conn.sendto("Hello, client".encode(), address)
    conn.close()


if __name__ == "__main__":
    main()
```
