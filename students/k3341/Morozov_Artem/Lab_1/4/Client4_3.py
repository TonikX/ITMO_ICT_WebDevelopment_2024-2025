import socket
import threading


def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(message)


def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))


def start_client(host='127.0.0.1', port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Подключено к серверу.")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    name = input("Введите своё имя: ")
    client_socket.send(name.encode('utf-8'))

    send_messages(client_socket)

if __name__ == "__main__":
    start_client()
