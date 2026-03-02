# Задание
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно
отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно
отобразиться у клиента.

**Требования:**

 - Обязательно использовать библиотеку socket.
 - Реализовать с помощью протокола UDP.
 
***

# Решение

## Клиент

```python
import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("Hello, server!".encode(), (HOST, PORT))
    data, addr = sock.recvfrom(1024)
    print("Server:", data.decode())
    sock.close()

if __name__ == '__main__':
    main()

```

## Сервер

```python
import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print("UDP server is running...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received from {addr}: {data.decode()}")
        sock.sendto("Hello client!".encode(), addr)


if __name__ == "__main__":
    main()

```

***

# Пояснение

Создаём UDP сокет на сервере, используя адрес `127.0.0.1` и порт `9090`, после чего в бесконечном цикле пытаемся прочитать данные от
клиента и напечатать их, а затем отправить сообщение `Hello, client` клиенту.

Клиент создает UDP сокет и без установки соединения отправляет данные на `127.0.0.1:9090`. Затем читает ответ от сервера и закрывает сокет.