import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}\n")
        except:
            print("Connection lost.")
            break


def send_messages(client_socket):
    while True:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))
        if not message:
            client_socket.close()
            break


def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))  # Подключение к серверу

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()


if __name__ == "__main__":
    client_program()
