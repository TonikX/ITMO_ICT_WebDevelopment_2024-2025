import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = {}
addresses = {}

def handle_client(client_socket, address):
    name = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = name
    addresses[client_socket] = address

    print(f'[{address}] Присоединился {name}')

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                send_to_all(f'{name}: {data}', client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break

def send_to_all(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                remove_client(client_socket)

def remove_client(client_socket):
    name = clients[client_socket]
    address = addresses[client_socket]
    del clients[client_socket]
    del addresses[client_socket]
    client_socket.close()
    print(f'[{address}] {name} отключился')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'Сервер запущен на {HOST}:{PORT}')

    while True:
        client_socket, address = server_socket.accept()
        print(f'Подключение установлено с {address}')
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()