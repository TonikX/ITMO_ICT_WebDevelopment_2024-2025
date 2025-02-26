# Задание 4

## Текст задания

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.
## Требования

*   Обязательно использовать библиотеку `socket`.
*   Для многопользовательского чата необходимо использовать библиотеку `threading`.

## Код

### client.py

    import socket
    import threading

    nickname = input("Введите свой никнейм: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 1111))

    def receive():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    client.send(nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Произошла ошибка!")
                client.close()
                break

    def write():
        while True:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('utf-8'))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

### server.py

    import socket
    import threading

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1111))
    server.listen()

    clients = []
    nicknames = []

    def broadcast(message):
        for client in clients:
            client.send(message)

    def handle(client):
        while True:
            try:
                message = client.recv(1024)
                broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} покинул(а) чат!'.format(nickname).encode('utf-8'))
                nicknames.remove(nickname)
                break

    def receive():
        while True:
            client, address = server.accept()
            print("Подключился {}".format(str(address)))

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)

            print("Никнейм: {}".format(nickname))
            broadcast("{} присоединился(ась)!".format(nickname).encode('utf-8'))
            client.send('Подключено к серверу!'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    receive()