Задание 1: 
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола UDP.

Листинг кода серверной части:

```python
import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("127.0.0.1", 9090))  # порт 9090
udp_server.settimeout(1)  # тайм-аут до 1

try:
    while True:
        try:
            message, client_address = udp_server.recvfrom(1024)
            print(f"Received message: {message.decode()}")
            udp_server.sendto("Hello, client".encode(), client_address)
        except socket.timeout:
            pass  # пропускаем время ожидания

except KeyboardInterrupt:
    udp_server.close()
    print("Server closed.")

```

Листинг кода клиентской части:

```python
import socket

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_client.sendto("Hello, server".encode(), ("127.0.0.1", 9090))
response, server_address = udp_client.recvfrom(1024)
print(f"Message: {response.decode()}")

Объяснение: 

1. С помощью socket.socket(socket.AF_INET, socket.SOCK_DGRAM) создаём объект сокета, где socket.AF_INET отвечает за IPv4, а socket.SOCK_DGRAM за протокол UDP.
2. Задаём .timeout (1)
3. Используем .recvfrom для получения данных и адреса клиента, а .sendto для возвращения ответа.
4. Имеющийся код в try-except socket.timeout, чтобы таймаут не завершил работу сервера.
5. Задействованный try-except в цикл while True, чтобы сервер не прекратил работу после обработки первого запроса.
6. Цикл в try-except KeyboardInterrupt, чтобы можно было завершить работу сервера по нажатию на сочетание клавиш Ctrl+C.