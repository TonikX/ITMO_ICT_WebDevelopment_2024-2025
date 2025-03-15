# Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно 
отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно 
отобразиться у клиента.

## Файл server.py

[ссылка](../task_1/server.py)

Код из файла:

```python
import socket
import signal


def raise_timeout(signum, frame):
    """
    Функция для рейза ошибки таймаута
    :param signum:
    :param frame:
    :return:
    """
    raise TimeoutError


if __name__ == '__main__':

    signal.signal(signal.SIGALRM, raise_timeout)

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('', 8088)
    socket_server.bind(server_address)

    signal.alarm(60)  # убиваем таймаутом после минуты ожидания

    try:
        while True:
            data, address = socket_server.recvfrom(1024)
            print(f"Client with ip {address[0]} and port {address[1]} sent a message: {data.decode()}")

            response = "Hello, client"
            socket_server.sendto(response.encode(), address)
            break
    finally:
        signal.alarm(0)

```

Был реализован сервер, через UDP получающий сообщение от клиента
и через него же получающий ответ.

Также была реализована проверка на таймаут с помощью библиотеки `signal`

[Скрин работы сервера](imgs/task1_server.png)

[Скрин ошибки таймаута](imgs/task1_server_error.png)

## Файл client.py

Код из файла:

```python
import socket

if __name__ == '__main__':
    socket_user = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 8088)
    message = 'Hello, server'
    socket_user.sendto(message.encode(), server_address)

    data, server = socket_user.recvfrom(1024)
    socket_user.close()

    print(data.decode())
```

[Скрин работы клиента](imgs/task1_client.png)