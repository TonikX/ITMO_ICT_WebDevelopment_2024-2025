# Задание 4

## Суть задания

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат

**Требования**:
- Обязательно использовать библиотеку socket
- Для многопользовательского чата необходимо использовать библиотеку threading

## Код программы

### Клиент

```python
import socket
import threading

PORT = 1313
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 1024


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def client_receive():
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode()
            print(message)
        except:
            print('Error')
            client.close()
            break

def client_send():
    while True:
        message = f'{input()}'
        client.send(message.encode(FORMAT))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
```

### Сервер
```python
import socket
import threading

PORT = 1313
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(BUFFER_SIZE)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break

def receive():
    while True:
        print('Server is running and listening...')
        client, addr = server.accept()
        print(f'Connection is established with {str(addr)}')
        clients.append(client)
        broadcast(f'{str(addr)} has entered the room'.encode(FORMAT))
        client.send('You are now connected'.encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
```