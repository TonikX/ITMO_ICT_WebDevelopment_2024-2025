import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

def listen_for_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("Соединение с сервером потеряно.")
                break
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Запуск отдельного потока для получения сообщений от сервера
    threading.Thread(target=listen_for_messages, args=(client_socket,)).start()

    # Основной цикл отправки сообщений
    while True:
        user_input = input()

        if user_input.lower() == "покинуть чат":
            break

        try:
            client_socket.send(user_input.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
