import socket
import threading

HOST = '127.0.0.1'  # Адрес сервера
PORT = 12345        # Порт сервера

def receive_messages(sock):
    # Функция для получения сообщений от сервера.
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(f"Получено сообщение: {message}")
            else:
                break
        except:
            print("Соединение закрыто.")
            break

def start_client():
    # Функция для запуска клиента.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Запуск потока для получения сообщений
    threading.Thread(target=receive_messages, args=(sock,)).start()
    threading.Thread(target=send_messages, args=(sock,)).start()


def send_messages(sock):
    # Отправка сообщений
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        sock.send(message.encode())
    sock.close()

if __name__ == "__main__":

    start_client()