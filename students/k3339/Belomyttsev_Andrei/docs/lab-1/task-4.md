# Task 4

## Задание
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

**Требования:**

  - Обязательно использовать библиотеку `socket`.
  - Для многопользовательского чата необходимо использовать библиотеку `threading`.

**Реализация:**

  - Протокол TCP: 100% баллов.
  - Протокол UDP: 80% баллов.
  - Для UDP используйте `threading` для получения сообщений на клиенте.
  - Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

**Полезные ссылки:**

  - [Документация Python: threading](https://docs.python.org/3/library/threading.html)
  - [WebDevBlog: Введение в потоки Python](https://webdevblog.ru/vvedenie-v-potoki-v-python/)

---

## TCP multiplayer chat

You can choose specific IP address and port by changing `IP` and `PORT` variables.

Firstly run `python 4-server.py`

Then run multiple `python 4-client.py`

Enter name on client. Then you will be able to send and receive messages.

Server:
```
Chat started...
('127.0.0.1', 52188) connected
Name is Andrei
('127.0.0.1', 52195) connected
Name is Alice
('127.0.0.1', 52499) connected
Name is Dima
```

Client 1:
```
Enter name: Andrei
Andrei joined the chat.
Alice joined the chat.
Dima joined the chat.
Hello!
Andrei: Hello!
Alice: Hi!
Dima: Hello World!
```

Client 2:
```
Enter name: Alice 
Alice joined the chat.
Dima joined the chat.
Andrei: Hello!
Hi!   
Alice: Hi!
Dima: Hello World!
```

Client 3:
```
Enter name: Dima 
Dima joined the chat.
Andrei: Hello!
Alice: Hi!
Hello World!
Dima: Hello World!
```

---

## Code

4-server.py:
```python
import socket
import threading

IP = '127.0.0.1'
PORT = 2020

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

clients = []
names = []

def broadcast(message):
  for i in clients:
    i.send(message)

def handle(client):
  while True:
    try:
      index = clients.index(client)
      name = names[index]
      message = client.recv(1024)
      if message:
        message = f'{name}: '.encode('utf-8') + message
        broadcast(message)
    except:
      clients.remove(client)
      client.close()
      broadcast(f'{name} left the chat.'.encode('utf-8'))
      names.remove(name)
      break

def connect():
  while True:
    client, address = server.accept()
    print(address, 'connected')
    client.send('NAME'.encode('utf-8'))
    name = client.recv(1024).decode('utf-8')
    names.append(name)
    clients.append(client)
    print('Name is', name)
    broadcast(f'{name} joined the chat.'.encode('utf-8'))
    threading.Thread(target=handle, args=(client,)).start()

print('Chat started...')
connect()
```

4-client.py:
```python
import socket
import threading

IP = '127.0.0.1'
PORT = 2020

name = input('Enter name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

def get():
  while True:
    try:
      message = client.recv(1024).decode('utf-8')
      if message == 'NAME':
        client.send(name.encode('utf-8'))
      else:
        print(message)
    except Exception as e:
      print(e)
      client.close()
      break

def send():
  while True:
    message = input()
    client.send(message.encode('utf-8'))

threading.Thread(target=get).start()
threading.Thread(target=send).start()
```