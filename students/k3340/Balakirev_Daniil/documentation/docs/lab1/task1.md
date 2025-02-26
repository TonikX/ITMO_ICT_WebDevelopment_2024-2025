# Задание 1

## Текст задания

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## Требования

*   Обязательно использовать библиотеку `socket`.
*   Реализовать с помощью протокола UDP.

## Код

### client.py

    import socket

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 1234)

    message = 'Hello server'
    client.sendto(message.encode(), server_address)

    data, server = client.recvfrom(1024)
    print(f'Ответ от сервера: {data.decode()}')

    client.close()


### server.py

    import socket

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 1234))
    print("Сервер запущен, ожидает подключения...")

    conn, addr = server.recvfrom(1024)
    request = conn.decode()
    print(f'Запрос от {addr}: {request}')

    response = 'Hello client'
    server.sendto(response.encode(), addr)

    server.close()