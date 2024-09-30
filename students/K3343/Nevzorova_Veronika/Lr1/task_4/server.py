import socket
import threading

def broadcast_message(message, current_client):
    # Рассылка сообщения всем клиентам, кроме текущего
    for user in connected_users:
        if user != current_client:
            try:
                user.send(message)
            except:
                user.close()
                remove_client(user)

def handle_client_connection(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Получено сообщение от клиента: {message.decode('utf-8')}")
                broadcast_message(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue

def remove_client(client_socket):
    if client_socket in connected_users:
        connected_users.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('0.0.0.0', 8075))
        print(f"Сервер запущен на порту 8075")
        server_socket.listen()
        print("Ожидание подключений...")
    except Exception as error:
        print(f"Ошибка запуска сервера: {error}")
        return

    while True:
        try:
            socket_user, user_address = server_socket.accept()
            print(f"Подключён клиент с адреса: {user_address}")
            connected_users.append(socket_user)
            threading.Thread(target=handle_client_connection, args=(socket_user,)).start()
        except Exception as error:
            print(f"Ошибка при подключении клиента: {error}")

if __name__ == "__main__":
    connected_users = []
    start_server()
