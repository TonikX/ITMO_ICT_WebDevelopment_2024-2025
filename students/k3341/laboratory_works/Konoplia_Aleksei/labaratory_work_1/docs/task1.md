# Задание 1

## UDP Клиент-Сервер

### Задание:

реализовать клиентскую и серверную часть приложения. Клиент отправляет сообщение "Hello server", которое должно отображаться на стороне сервера. В ответ сервер отправляет клиенту сообщение "Hello client", которая отоборжается у пользователя.

1. Запуск сервера
``` bash 
python task1/udp_server_hello.py
```

2. Запуск клиента
``` bash 
python task1/udp_client_hello.py
```

### Сервер
``` python
import socket

def udp_server_hello():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 12345))
    print("UDP сервер запущен на порту 12345")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Получено сообщение: {message.decode()} от {client_address}")
        server_socket.sendto(b"Hello, client", client_address)

if __name__ == '__main__':
    udp_server_hello()
```


### Клиент

``` python
import socket

def udp_client_hello():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(b"Hello, server", ("localhost", 12345))
    response, _ = client_socket.recvfrom(1024)
    print(f"Ответ сервера: {response.decode()}")
if __name__ == '__main__':
    udp_client_hello()
```