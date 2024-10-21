### Задание 1:

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

- Обязательно использовать библиотеку socket.

- Реализовать с помощью протокола UDP.


### Ход работы:

#### server.py

```
import socket


def start_udp_server():
    serv_address = ('localhost', 8080)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(serv_address)
        print('Сервер запущен и подключен по адресу:', serv_address)

        while True:
            data, cl_address = sock.recvfrom(1024)
            print('Получено сообщение от клиента:', data.decode())
            response = 'Hello, client!'
            sock.sendto(response.encode(), cl_address)
            print('Отправлено сообщение клиенту:', response)


if __name__ == "__main__":
    start_udp_server()
```


#### client.py

```
import socket


def communicate_with_server():
    serv_address = ('localhost', 8080)
    message = 'Hello, server!'

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), serv_address)
        print(f'Message sent to server: {message}')

        data, _ = sock.recvfrom(1024)
        print(f'Received message from server: {data.decode()}')


if __name__ == "__main__":
    communicate_with_server()

```

Для успешного обмена данными сначала необходимо запустить серверный файл, который всегда готов 
слушать, а потом запустить клиентский файл, который сразу после установки соединения отправляет 
сообщение.

UDP соединение обеспечивается созданием UDP-socket с помощью параметра `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`
