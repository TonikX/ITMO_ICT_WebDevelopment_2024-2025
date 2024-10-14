import socket
import threading

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, client_address):
    try:
        client_socket.send("Введите ваше имя: ".encode())
        name = client_socket.recv(1024).decode()
        
        welcome_message = f"{name} подключился к чату!"
        print(welcome_message)
        broadcast(welcome_message.encode(), client_socket)

        while True:
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
        client_socket.close()
        clients.remove(client_socket)
        leave_message = f"{name} отключился."
        print(leave_message)
        broadcast(leave_message.encode(), None)

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

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
