import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("Произошла ошибка при получении сообщения.")
            client_socket.close()
            break


def send_messages(client_socket):
    while True:
        message = input("")
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            print("Произошла ошибка при отправке сообщения.")
            client_socket.close()
            break


def start_client(host='127.0.0.1', port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    name = input("Введите ваше имя: ")
    client_socket.send(name.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


if __name__ == "__main__":
    start_client()
