import socket
import threading

HOST = 'localhost'
PORT = 9091

clients = []
client_names = []

def handle_client(client_socket, client_address):
    print(f"Установлено новое соединение с: {client_address}")
    client_socket.send("Пожалуйста, введите ваше имя:".encode('utf-8'))

    username = client_socket.recv(1024).decode('utf-8')
    client_names.append(username)
    clients.append(client_socket)

    broadcast_message(f"{username} присоединился к чату.".encode('utf-8'))

    # Основной цикл для обработки сообщений клиента
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast_message(f"{username}: {message.decode('utf-8')}".encode('utf-8'))
            else:
                remove_client(client_socket)
                break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            remove_client(client_socket)
            break

# Функция для отправки сообщения всем пользователям
def broadcast_message(message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            remove_client(client)

# Функция для удаления отключенного клиента
def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        username = client_names[index]
        clients.remove(client_socket)
        client_names.remove(username)
        print(f"{username} отключился от чата.")
        broadcast_message(f"{username} вышел из чата.".encode('utf-8'))

# Запуск сервера
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на {HOST}:{PORT} и ожидает подключения...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    run_server()