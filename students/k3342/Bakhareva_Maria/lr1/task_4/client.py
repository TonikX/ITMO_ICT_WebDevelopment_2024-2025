import socket
import threading

def receive_messages(client_socket):
    """Получает сообщения от сервера."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Ошибка при получении сообщения.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Запускаем поток для получения сообщений
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode())

    client_socket.close()

start_client()
