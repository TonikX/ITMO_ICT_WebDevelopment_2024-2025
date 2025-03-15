import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def receive_messages(client_socket):
    """Получает и выводит сообщения от сервера."""
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Соединение с сервером потеряно.")
            break
    client_socket.close()

def tcp_client():
    """Запуск TCP-клиента."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Подключено к серверу.")

        thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        thread.start()

        while True:
            message = input()
            if message.lower() == "exit":
                print("Отключение от сервера.")
                break
            try:
                client_socket.send(message.encode())
            except BrokenPipeError:
                print("Соединение с сервером разорвано.")
                break

if __name__ == "__main__":
    tcp_client()
