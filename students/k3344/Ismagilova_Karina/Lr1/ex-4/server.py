import socket
import threading

HOST = 'localhost'
PORT = 8080

clients = {}

def broadcast(message, sender_socket):
    for client_socket in clients.keys():
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
                disconnect_client(client_socket)

def disconnect_client(client_socket):
    client_name = clients.pop(client_socket, "Агент под прикрытием")
    client_socket.close()
    print(f"{client_name} отключился.")
    broadcast(f"{client_name} вышел из чата :(".encode('utf-8'), client_socket)

def handle_client(client_socket, client_address):
    print(f"[{client_address}] подключился.")
    client_socket.send("Ваше имя: ".encode('utf-8'))
    client_name = client_socket.recv(1024).decode('utf-8').strip() or "Агент под прикрытием"

    clients[client_socket] = client_name
    welcome_message = f"{client_name} теперь в чате!".encode('utf-8')
    broadcast(welcome_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                full_message = f"{client_name}: {message.decode('utf-8')}".encode('utf-8')
                broadcast(full_message, client_socket)
            else:
                disconnect_client(client_socket)
                break
        except Exception as e:
            disconnect_client(client_socket)
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Сервер запущен")
    try:
        while True:
            client_socket, client_address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        print("\nСервер завершает работу.")
    finally:
        for client in clients:
            client.close()
        server.close()

if __name__ == "__main__":
    start_server()
