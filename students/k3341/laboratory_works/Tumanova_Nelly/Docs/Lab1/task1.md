# Задание №1: Обмен сообщениями по UDP

## Постановка задачи

Реализовать клиентскую и серверную часть приложения.
Клиент отправляет серверу сообщение `«Hello, server»`, и оно должно отобразиться
на стороне сервера. В ответ сервер отправляет клиенту сообщение `«Hello, client»`,
которое должно отобразиться у клиента.

Требования:

- [x] Обязательно использовать библиотеку socket
- [x] Реализовать с помощью протокола UDP

## Выполнение

### `server.py`

```python
import socket

SERVER_ADDR = ("localhost", 9090)

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(SERVER_ADDR)

    print(f"[*] UDP-server started on {SERVER_ADDR[0]}:{SERVER_ADDR[1]}")

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"[Message from {client_address[0]}:{client_address[1]}] {message}")

            response = "Hello, client!"
            server_socket.sendto(response.encode('utf-8'), client_address)
    except KeyboardInterrupt:
        print("[*] UDP-server stopped")
    finally:
        server_socket.close()
```

`socket.socket(AF_INET, SOCK_DGRAM)` — создаёт UDP-сокет для IPv4.
`AF_INET` — семейство адресов IPv4, `SOCK_DGRAM` — дейтаграммный сокет (UDP).

`bind(address)` — привязывает сокет к адресу `localhost:9090`. После этого ядро ОС направляет все UDP-пакеты на этот
порт в данный сокет. Для сервера обязателен.

`recvfrom(bufsize)` — блокирующий приём дейтаграммы. Возвращает кортеж `(data, address)`, где `data` — байты payload,
`address` — кортеж `(ip, port)` отправителя. Нужен, чтобы знать, куда отправить ответ.

`decode('utf-8')` — превращает байты в строку для вывода на консоль.

`sendto(data, address)` — отправляет дейтаграмму по указанному адресу. `encode('utf-8')` превращает строку в байты.

`KeyboardInterrupt` / `finally` — корректное завершение по `Ctrl+C` с закрытием сокета.

### `client.py`

```python
import socket

SERVER_ADDR = ("localhost", 9090)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "Hello, server!"
    client_socket.sendto(message.encode('utf-8'), SERVER_ADDR)

    client_socket.settimeout(5.0)
    try:
        data, server_address = client_socket.recvfrom(1024)
        response = data.decode('utf-8')
        print(f"[Message from {server_address[0]}:{server_address[1]}] {response}")
    except socket.timeout:
        print("[Error] Server timeout")

    client_socket.close()
```

`socket.socket(AF_INET, SOCK_DGRAM)` — создаёт UDP-сокет, как и на сервере. Клиент не вызывает `bind()` — ОС сама
назначит случайный эфемерный порт, чтобы было куда вернуть ответ.

`sendto(data, address)` — отправляет дейтаграмму на `localhost:9090`. Соединение не устанавливается.

`settimeout(5.0)` — задаёт таймаут для блокирующих операций сокета. Без него `recvfrom()` ждал бы ответа вечно, если
сервер не запущен.

`recvfrom(bufsize)` — принимает ответную дейтаграмму от сервера. При превышении таймаута выбрасывает `socket.timeout`.

`decode('utf-8')` — декодирует байты ответа в строку.

`close()` — закрывает сокет и освобождает ресурсы.

## Вывод

В ходе работы изучены базовые функции модуля `socket` для UDP:

- `socket()` — создание UDP-сокета;
- `bind()` — привязка к адресу (сервер);
- `sendto()` — отправка дейтаграммы;
- `recvfrom()` — приём дейтаграммы и адреса отправителя;
- `settimeout()` — защита от бесконечного ожидания;
- `close()` — освобождение сокета.

UDP не устанавливает соединение: сервер не использует `listen()`/`accept()`, а клиент — `connect()`. Обмен идёт
отдельными дейтаграммами, что делает код компактнее, но не даёт гарантий доставки.