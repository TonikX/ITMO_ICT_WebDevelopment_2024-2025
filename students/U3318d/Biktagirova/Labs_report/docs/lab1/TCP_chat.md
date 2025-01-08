## Задание 4:
Реализовать многопользовательский чат.

### Требования:

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.

`Server's code`
```py
import socket
import threading

PORT = 8080
HOST = 'localhost'
BUFF_SIZE = 1024

clients = []
nicks = []


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                print(f"Error sending message to {client}")


def receive(server):
    while True:
        try:
            client_conn, address = server.accept()
            print(f'{address} has connected')

            nick = client_conn.recv(BUFF_SIZE).decode()
            nicks.append(nick)
            clients.append(client_conn)

            client_conn.send(f'Welcome to chat,{nick} :)'.encode())

            joined_message = f'{nick} joined our chat!'
            broadcast(joined_message.encode(), client_conn)

            thread = threading.Thread(target=handle, args=(client_conn, nick))
            thread.start()
        except:
            print(f"Error accepting client")


def handle(client, nickname):
    while True:
        try:
            message = client.recv(BUFF_SIZE)
            if not message:
                remove(client, nickname)
                break

            broadcast(message, client)
        except:
            print(f"Error handling message from {nickname}")
            remove(client, nickname)
            break


def remove(client, nickname):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nicks.pop(index)
        leave_message = f'{nickname} left the chat :('
        broadcast(leave_message.encode(), client)


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f'TCP server is running on {HOST}:{PORT}')
    receive(server_socket)
```
### Client's code

```py
import socket
import threading


def receive(client):
    while True:
        try:
            message = client.recv(BUFF_SIZE).decode()
            if message:
                print(message)
            else:
                print("Server has closed the connection.")
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    client.close()
    exit()


def write(client, nickname):
    while True:
        try:
            message = f'{nickname}: {input("")}'
            client.send(message.encode())
        except:
            print(f"Error sending message")
            break


if __name__ == '__main__':
    PORT = 8080
    HOST = 'localhost'
    BUFF_SIZE = 1024

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except:
        print(f"Error connecting to server")
        exit()

    nick = input("Welcome to the chat! What's your nickname? ")

    client_socket.send(nick.encode())

    receive_th = threading.Thread(target=receive, args=(client_socket,))
    receive_th.start()

    write_th = threading.Thread(target=write, args=(client_socket, nick))
    write_th.start()

    receive_th.join()
    write_th.join()
```