# Реализовать клиентскую и серверную часть приложения. Клиент отсылает серверу
# сообщение «Hello, server». Сообщение должно отразиться на стороне сервера.
# Сервер в ответ отсылает клиенту сообщение «Hello, client». Сообщение должно
# отобразиться у клиента.
# Обязательно использовать библиотеку socket
# Реализовать с помощью протокола UDP

import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.bind(('127.0.0.1', 14900))

data = conn.recvfrom(16384)
udata = data[0].decode('utf-8')
print(f'Message: {udata}')
print('Response: Hello, client')

conn.close()