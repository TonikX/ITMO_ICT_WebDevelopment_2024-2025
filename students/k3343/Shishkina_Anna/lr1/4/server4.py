import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    print(f"Подключился пользователь {client_address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            full_message = f"{client_address[1]} {message}"
            print(full_message)
            broadcast_message(full_message, client_socket)
        except Exception as e:
            print(f"Ошибка с пользователем {client_address}: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"{client_address} отключился")

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Ошибка отправки сообщения: {e}")
                client.close()
                clients.remove(client)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Сервер запущен")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
