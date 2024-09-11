import socket
import threading

green_s = '\033[32m'
red_s = '\033[31m'
green_e = '\033[0m'
red_e = '\033[0m'
users = {}


def broadcast(message, sender_socket=None, target_user=None):
    if target_user:
        target_socket = users.get(target_user)
        if target_socket:
            try:
                target_socket.send(message)
            except:
                target_socket.close()
                del users[target_user]
                print(f"{red_s}Ошибка при отправке сообщения пользователю {target_user}{red_e}")
        else:
            print(f"{red_s}Пользователь {target_user} не найден{red_e}")
            sender_socket.send(f"{red_s}Ошибка: Пользователь {target_user} не найден{red_e}".encode('utf-8'))
        return

    for user, client_socket in users.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del users[user]


def handle_client(client_socket, client_address):
    print(f"Новое подключение: {client_address}")

    client_socket.send("Введите своё имя: ".encode('utf-8'))
    user_name = client_socket.recv(1024).decode('utf-8')
    if user_name in users:
        client_socket.send("Имя уже занято, подключение прервано.\n".encode('utf-8'))
        client_socket.close()
        return
    users[user_name] = client_socket

    broadcast(f"{green_s}{user_name} присоединился к чату.{green_e}".encode('utf-8'), client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"{user_name}: {message.decode('utf-8')}")

            if message.decode('utf-8').startswith("@"):
                target_user, personal_message = message.decode('utf-8').split(' ', 1)
                target_user = target_user[1:]
                broadcast(
                    f"{user_name} {green_s}(лично для {target_user}){green_e}: {personal_message}".encode('utf-8'),
                    client_socket, target_user=target_user)
            else:
                broadcast(f"{user_name}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
        except:
            client_socket.close()
            del users[user_name]
            broadcast(f"{red_s}{user_name} покинул чат.{red_e}".encode('utf-8'))
            break


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 1234))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


start_server()
