import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
ENCODING = 'utf-8'


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode(ENCODING)
            if message == 'margo':
                client_socket.send(nickname.encode(ENCODING))
            else:
                print(message)
        except OSError:
            print("An error occurred while receiving data!")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = f'{nickname}: {input("")}'
        client_socket.send(message.encode(ENCODING))


if __name__ == "__main__":
    nickname = input("Choose your nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionError:
        print("Failed to connect to the server.")
        exit()

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    write_thread = threading.Thread(target=send_messages, args=(client,))
    write_thread.start()
