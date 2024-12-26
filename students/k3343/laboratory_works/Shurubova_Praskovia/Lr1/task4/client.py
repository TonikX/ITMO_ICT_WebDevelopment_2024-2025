import socket
import threading

def receive_messages(client_socket):
    """Функция для получения сообщений от сервера"""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode('utf-8'))
            else:
                break
        except:
            print("Вы потеряли соединение с сервером.")
            break

def start_client():
    """Функция для запуска клиента"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        message = input('')
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()
