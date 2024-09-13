# Задание 1: UDP клиент-сервер

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  

Требования:  
- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола `UDP`.

## Файлы
- `udp_server.py`: Реализация UDP сервера
```python
import socket

buffer_size = 1024
port = 8080
host = 'localhost'
server_address = (host, port)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    print(f"UDP server has started on {host}:{port}")

    while True:
        message, client_address = server_socket.recvfrom(buffer_size)
        print(f"Client message: {message.decode()}")
        server_socket.sendto(b"Hello client", client_address)

    server_socket.close()

if __name__ == "__main__":
    server()
```
- `udp_client.py`: Реализация UDP клиента
```python
import socket

buffer_size = 1024
port = 8080
host = 'localhost'
server_address = (host, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(b"Hello server", server_address)
response, server = client_socket.recvfrom(buffer_size)
print(f"Ответ от сервера: {response.decode()}")

client_socket.close()
```
