### Задание 4:

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.
Реализация:
Протокол TCP: 100% баллов.
Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

### Ход работы:

#### server.py

```
import socket
import threading

clients = []
names = []


def client_handler(client_socket):
    while True:
        try:
            text = client_socket.recv(1024).decode()
            if text == 'leave':
                leave_chat(client_socket)
            elif text:
                print(str(text))
                send_text(text, client_socket)
        except:
            continue


def send_text(text, client_socket):
    for client in clients:
        if client != client_socket:
            index = clients.index(client_socket)
            name = names[index]
            client.send(f'{name}: {text}'.encode())


def leave_chat(client_socket):
    send_text('has abandoned y\'all', client_socket)
    ind = clients.index(client_socket)
    clients.remove(client_socket)
    name = names[ind]
    names.remove(name)
    print(f'{name} left')


serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
serv_sock.bind(serv_address)
serv_sock.listen()
print('server is connected and listening:', serv_address)

while True:
    cl_socket, cl_address = serv_sock.accept()
    cl_socket.send('what\'s your name:'.encode())
    name = cl_socket.recv(1024).decode()
    names.append(name)
    clients.append(cl_socket)
    print(f'{name} joined')
    send_text('is amongst you now', cl_socket)

    thread = threading.Thread(target=client_handler, args=(cl_socket, ))
    thread.start()
```


#### client.py

```
import socket
import threading


def get_text(client_socket):
    while True:
        try:
            other_text = client_socket.recv(1024).decode()
            if other_text:
                print(str(other_text))
            else:
                break
        except:
            break


cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
cl_socket.connect(serv_address)

thread = threading.Thread(target=get_text, args=(cl_socket, ))
thread.start()

while True:
    text = input("")
    cl_socket.send(text.encode())
    if text == 'leave':
        cl_socket.close()
        break

```

TCP соединение обеспечивается созданием TCP-socket с помощью параметра `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`

В серверной части чата после определения соединения прописываем основную функцию работы с 
клиентами: приём сообщений пользователя с условиями. Сначала транслируется присоединение 
пользователя к беседе. Если клиент желает выйти из чата с помощью 
кодового слова, то эта новость распространяется между другими пользователями и клиент удаляется 
из списка участников чата и его связь обрывается. В ином случае, если клиент отправил обычное 
сообщение, то оно транслируется другим участникам чата с именем отправителя.

В клиентской части прописывается получение чужих сообщений и объявлений сервера. При попытке 
выйти из чата связь пользователя с сервером обрывается.