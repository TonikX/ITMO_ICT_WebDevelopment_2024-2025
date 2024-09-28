import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

# Хранилище
connected_clients = []
client_names = []

# Обработчик клиента
def start_connection(client_socket, client_address):
    print(f"Новое подключение: {client_address}")
    client_socket.send("Введите своё имя:".encode('utf-8'))

    # Ожидаем, пока клиент отправит своё имя
    username = client_socket.recv(1024).decode('utf-8')
    client_names.append(username)
    connected_clients.append(client_socket)

    # Оповещаем всех о новом участнике
    send_message(f"{username} присоединился к чату.".encode('utf-8'))

    # Основной цикл получения сообщений
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                send_message(f"{username}: {message.decode('utf-8')}".encode('utf-8'))
            else:
                remove_user(client_socket)
                break
        except Exception as e:
            print(f"Ошибка: {e}")
            remove_user(client_socket)
            break

# Функция рассылки сообщений всем клиентам
def send_message(message):
    for client in connected_clients:
        try:
            client.send(message)
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            remove_user(client)
def remove_user(client_socket):
    if client_socket in connected_clients:
        index = connected_clients.index(client_socket)
        disconnected_user = client_names[index]
        connected_clients.remove(client_socket)
        client_names.remove(disconnected_user)
        print(f"{disconnected_user} покинул чат.")
        send_message(f"{disconnected_user} вышел из чата.".encode('utf-8'))

# Настройка сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")

    # Главный цикл подключения клиентов
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=start_connection, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
