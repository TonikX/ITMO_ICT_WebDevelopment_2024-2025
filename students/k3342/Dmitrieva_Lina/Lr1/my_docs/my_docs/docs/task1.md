# Задание 1: 

## Описание задачи

Реализовать клиентскую и серверную часть приложения, где клиент отправляет серверу сообщение «Hello, server», и сервер отвечает «Hello, client». Для реализации используется библиотека `socket` и протокол UDP.

## Код сервера
```python
import socket

server_address = ('localhost', 8080)
#Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Привязываем к локальному адресу и порту
server_socket.bind(server_address)
#Сервер говорит, что готов к работе
print('Сервер запущен на порте и ждет сообщений')

#В бесконечном цикле сервер ожидает сообщения от клиентов. Когда сообщение получено, оно выводится на экран, а сервер отправляет ответ «Hello, client» обратно клиенту.
while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f'Получено сообщение от клиента: {message.decode()}')

    if message:
        response = 'Hello, client!'
        server_socket.sendto(response.encode(), client_address)
        print(f'Отправлено сообщение клиенту: {response}')
```
## Код клиента
```python
import socket

server_address = ('localhost', 8080)
#Создаем сокет с использованием протокола UDP.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Отправляем сообщение «Hello, server» на локальный адрес сервера на порт
try:
    message = 'Hello, server'
    print(f'Отправка сообщения серверу: {message}')
    sent = server_socket.sendto(message.encode(), server_address)

    message, server = server_socket.recvfrom(1024)
    print(f'Получено сообщение от сервера: {message.decode()}')

finally:
    server_socket.close()
```