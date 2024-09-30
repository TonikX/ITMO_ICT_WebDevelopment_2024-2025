import socket
import threading

# Настройки клиента
host = 'localhost'
port = 14904

# Функция для получения сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}")
            else:
                break
        except:
            print("Ошибка получения сообщения.")
            client_socket.close()
            break

# Подключение к серверу и отправка сообщений
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Поток для получения сообщений от сервера
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Отправка сообщений на сервер
    while True:
        message = input("Введите сообщение: ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    start_client()
