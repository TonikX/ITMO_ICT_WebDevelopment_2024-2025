import socket
import threading

HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 4


def receive_messages(client_socket):
    while True:
        try:
            message_length_data = client_socket.recv(BUFFER_SIZE)
            if not message_length_data:
                continue
            message_length = int.from_bytes(message_length_data, byteorder="big")
            message = client_socket.recv(message_length).decode('utf-8')
            if message:
                print(f"\n{message}")
        except:
            print("[-] Ошибка соединения с сервером.")
            client_socket.close()
            break


username = input("Введите свой никнейм: ")
chat_id = input("Введите id чата: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()


def send_message(client_socket, msg):
    msg = msg.encode()
    msg_length = len(msg).to_bytes(BUFFER_SIZE, byteorder='big')
    client_socket.sendall(msg_length + msg)


send_message(client_socket, f"/setup_nickname {username}")
send_message(client_socket, f"/join_chat {chat_id}")

while True:
    try:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        send_message(client_socket, message)
    except KeyboardInterrupt:
        client_socket.close()
        break
