import socket
import threading

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"пользователь {client_address}:")
            print(message)
            if message:
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break


def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message.encode('utf-8'))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12366))
server_socket.listen(5)

print("Многопользовательский чат запущен...")

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Подключился {client_address}")

    threading.Thread(target=handle_client, args=(client_socket,)).start()

