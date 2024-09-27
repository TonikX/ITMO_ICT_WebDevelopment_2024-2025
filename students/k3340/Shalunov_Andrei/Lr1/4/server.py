import socket
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = sock.accept()
        print(f"Подключился новый пользователь с адресом {client_address}.")
        message = "Введите своё имя"
        client.send(message.encode())
        client_name = client.recv(1024).decode()
        clients[client_name] = client
        Thread(target=handle_client, args=(client, client_name)).start()


def handle_client(client, client_name):
    welcome_message = f"{client_name}, Добро пожаловать в чат"
    client.send(welcome_message.encode())
    message_other_clients = f"Внимание! В чат зашел новый пользователь с именем {client_name}"
    broadcast(message_other_clients, client_name)

    while True:
        try:
            message = client.recv(1024).decode()
            print(f"{client_name}: {message}")
            if message.lower() == "exit":
                goodbye_message = f"{client_name} покинул чат"
                broadcast(goodbye_message, client_name)
                client.close()
                del clients[client_name]
                break
            else:
                broadcast(f"{client_name}: {message}", client_name)
        except:
            print(f"Ошибка с клиентом {client_name}: {e}")
            goodbye_message = f"{client_name} покинул чат"
            broadcast(goodbye_message, client_name)
            client.close()
            del clients[client_name]
            break


def broadcast(msg, sender_name):
    if clients:
        for client_name, client_socket in clients.items():
            if client_name != sender_name:
                client_socket.sendall(msg.encode())


clients = {}

HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
print("Ждем подключений")
accept_thread = Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()
sock.close()
