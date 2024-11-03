import socket
import threading

# Функция для получения сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print("\n" + message)
            else:
                break
        except:
            print("Соединение с сервером было закрыто.")
            client_socket.close()
            break

# Функция для отправки сообщений серверу
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

# Подключаемся к серверу
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    print("Подключено к чату. Вы можете отправлять сообщения.")

    # Создаем потоки для отправки и получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    start_client()
