import socket
import threading
from dataclasses import dataclass

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024

members = []


@dataclass
class ChatMember:
    client_socket: socket
    username: str = None


def handle_client(client_socket, client_address):
    print(f"[+] Новое подключение от {client_address}")
    members.append(ChatMember(client_socket=client_socket))

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if message:
                member = find_chat_member(client_socket)
                print(f"[{client_address} :: {member.username}] {message}")

                if message[:16] == "/setup_nickname ":
                    if message[16:] == "":
                        client_socket.send("[SYSTEM] Ошибка: вы не можете установить пустой никнейм.".encode('utf-8'))
                        continue
                    if message[16:].lower() == "system" or message[-5:].lower() == "(you)":
                        client_socket.send("[SYSTEM] Ошибка: вы не можете установить этот никнейм.".encode('utf-8'))
                        continue
                    old_username = member.username
                    member.username = message[16:]
                    if old_username is None:
                        broadcast_message(f"{member.username} зашёл в чат.", None, system_msg=True)
                    else:
                        broadcast_message(f"{old_username} сменил никнейм на {member.username}", None, system_msg=True)
                    continue

                if member.username is None:
                    client_socket.send("[SYSTEM] Чтобы присоединиться к чату, вам нужно установить никнейм. Введите /setup_nickname <ваш никнейм>".encode('utf-8'))
                else:
                    broadcast_message(message, client_socket)
            else:
                break
        except ConnectionResetError:
            break

    print(f"[-] Отключен {client_address}")
    member = find_chat_member(client_socket)
    if member.username is not None:
        broadcast_message(f"{member.username} покинул чат.", client_socket, system_msg=True)
    remove_chat_member(client_socket)
    client_socket.close()


def find_chat_member(target_socket) -> ChatMember:
    for member in members:
        if member.client_socket == target_socket:
            return member
    return None

def remove_chat_member(target_socket):
    for member in members:
        if member.client_socket == target_socket:
            members.remove(member)
            break


def broadcast_message(message, sender_socket, system_msg: bool = False):
    sender = find_chat_member(sender_socket)
    for member in members:
        if member.username is not None:
            try:
                full_message = ("[SYSTEM]" if system_msg else f"[{sender.username}{' (You)' if member.client_socket == sender_socket else ''}]") + f" {message}"
                member.client_socket.send(f"{full_message}".encode('utf-8'))
            except:
                member.client_socket.close()
                members.remove(member)
                broadcast_message(f"{member.username} покинул чат.", client_socket, system_msg=True)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[*] Сервер запущен на {HOST}:{PORT}")

while True:
    client_socket, client_address = server.accept()

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
