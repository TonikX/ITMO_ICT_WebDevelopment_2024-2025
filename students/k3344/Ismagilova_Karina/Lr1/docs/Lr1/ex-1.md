## Задание № 1:
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента. 
Требования:
Использование библиотеки socket.
Реализовать с помощью протокола UDP.

### Стэк реализации:
- Язык - Python
- Библиотеки - socket
- Протокол - UDP

### Запуск программ:
Сервер:
```bash
    python server.py
```
Клиент:
```bash
    python client.py
```

### Листинг кода:

Сервер:
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))

print("Сервер запущен")

while True:
    request, client_address = server_socket.recvfrom(1024)
    print(f'Запрос от {client_address}: {request.decode()}')
    response = 'Hello, Client!'
    server_socket.sendto(response.encode(), client_address)
    # request.close()
```
Клиент:
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(b'Hello, server!', ('localhost', 8080))

response, server_address = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
```