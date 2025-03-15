import socket
import threading

# Настройки подключения
SERVER = 'localhost'
PORT = 12345

def receive_messages(client_socket):
    """Получение сообщений от сервера."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("[ERROR] Ошибка при получении сообщения.")
            break

def send_messages(client_socket):
    """Отправка сообщений серверу."""
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def main():
    """Главная функция для подключения к серверу и запуска потоков."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))

    # Получаем запрос на ввод имени
    server_message = client_socket.recv(1024).decode('utf-8')
    print(server_message)
    username = input()
    client_socket.send(username.encode('utf-8'))

    # Запускаем потоки для отправки и получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    main()
