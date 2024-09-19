import socket
import threading
import sys

HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 1024


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if message:
                print(f"\n{message}")
        except:
            print("[-] Ошибка соединения с сервером.")
            client_socket.close()
            break


username = input("Введите свой никнейм: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()
client_socket.send(f"/setup_nickname {username}".encode())

print("[*] Подключен к чату. Введите сообщения для отправки:")

while True:
    try:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        sys.stdout.write("\033[F")
        client_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        client_socket.close()
        break
