import socket
import threading


def receive_messages(client_socket):
    while True:
        try:

            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("[ERROR] Соединение с сервером потеряно")
            client_socket.close()
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Успешно подключен к серверу {SERVER_HOST}:{SERVER_PORT}")
except:
    print("Не удалось подключиться к серверу")
    exit()


user_name = input("Введите ваше имя: ")
client_socket.send(user_name.encode('utf-8'))


thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.start()

try:
    while True:

        message = input()
        if not message:
            print("Завершение работы")
            break
        client_socket.send(message.encode('utf-8'))
finally:
    client_socket.close()
    print("Клиент отключен")
