# Задание 4: 

## Описание задачи

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

## Код сервера
```python
import socket
import threading

#Список подключенных клиентов
clients = []

#Функция для рассылки сообщений всем клиентам
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

#Обработчик для каждого клиента
def handle_client(client_socket, client_address):
    try:
        # Получаем имя клиента
        client_socket.send("Введите ваше имя: ".encode())
        name = client_socket.recv(1024).decode()
        
        # Уведомляем всех о подключении нового клиента
        welcome_message = f"{name} подключился к чату!"
        print(welcome_message)
        broadcast(welcome_message.encode(), client_socket)

        while True:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024)
            if message:
                full_message = f"{name}: {message.decode()}"
                print(full_message)
                broadcast(full_message.encode(), client_socket)
            else:
                break
    except:
        pass
    finally:
        # Отключение клиента
        client_socket.close()
        clients.remove(client_socket)
        leave_message = f"{name} отключился."
        print(leave_message)
        broadcast(leave_message.encode(), None)

#Запуск сервера
def start_server():
    server_address = ('localhost', 8080)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen()

    print(f"Сервер запущен и ожидает подключения на порту {server_address[1]}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Клиент {client_address} подключен.")
        clients.append(client_socket)

        # Запускаем поток для обработки каждого клиента
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

#Запуск сервера
if __name__ == "__main__":
    start_server()
```
## Код клиента
```python
import socket
import threading

#Функция для получения сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Ошибка при получении сообщения.")
            client_socket.close()
            break

#Функция для отправки сообщений на сервер
def send_messages(client_socket):
    while True:
        message = input('')
        if message:
            try:
                client_socket.send(message.encode())
            except:
                print("Ошибка при отправке сообщения.")
                client_socket.close()
                break

#Подключение к серверу
def start_client():
    server_address = ('localhost', 8080)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # Получаем ввод имени пользователя и отправляем его на сервер
    name = input("Введите ваше имя: ")
    client_socket.send(name.encode())

    # Поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Поток для отправки сообщений
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

#Запуск клиента
if __name__ == "__main__":
    start_client()
```