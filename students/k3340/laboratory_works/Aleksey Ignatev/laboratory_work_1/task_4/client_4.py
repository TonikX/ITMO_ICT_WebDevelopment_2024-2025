import socket
import threading

HOST = '127.0.0.1'
PORT = 2003


def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message == 'exit':
            print("You've exited the cat.")
            break
        print(message)


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message == 'exit':
            break


if __name__ == "__main__":
    main()
