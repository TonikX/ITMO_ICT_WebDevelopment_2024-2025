import socket
import threading
import typing as tp
from dataclasses import dataclass

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 4

members = []


@dataclass
class ChatMember:
    client_socket: socket
    chat_id: str = None
    username: str = None


def handle_client(client_socket, client_address):
    print(f"[+] Новое подключение от {client_address}")
    members.append(ChatMember(client_socket=client_socket))

    while True:
        try:
            message_length_data = client_socket.recv(BUFFER_SIZE)
            if not message_length_data:
                continue
            message_length = int.from_bytes(message_length_data, byteorder="big")
            message = client_socket.recv(message_length).decode('utf-8')
            if message:
                member = find_chat_member(client_socket)
                print(f"[{client_address} :: {member.username}] {message}")

                if message[:16] == "/setup_nickname ":
                    if message[16:] == "":
                        send_message(client_socket, "[SYSTEM] Ошибка: вы не можете установить пустой никнейм.")
                        continue
                    if message[-6:].lower() == "system" or message[-5:].lower() == "(you)" or message[-4:].lower() in [
                        "none", "null"]:
                        send_message(client_socket, "[SYSTEM] Ошибка: вы не можете установить этот никнейм.")
                        continue
                    old_username = member.username
                    member.username = message[16:]
                    if member.username == old_username:
                        send_message(client_socket, "[SYSTEM] У вас уже установлен этот никнейм.")
                        continue
                    if member.chat_id is not None:
                        broadcast_message(f"{old_username} сменил никнейм на {member.username}", member.chat_id, None,
                                          system_msg=True)
                    continue
                elif message[:11] == "/join_chat ":
                    if member.username is None:
                        send_message(client_socket,
                                     "[SYSTEM] Чтобы присоединиться к чату, вам нужно установить никнейм. Введите /setup_nickname <ваш никнейм>")
                        continue
                    if message[11:] == "":
                        send_message(client_socket, "[SYSTEM] Ошибка: вы не можете установить пустой айди чата.")
                        continue
                    old_chat_id = member.chat_id
                    member.chat_id = message[11:]
                    if member.chat_id == old_chat_id:
                        send_message(client_socket, "[SYSTEM] Вы уже в этом чате.")
                        continue
                    if old_chat_id is not None:
                        broadcast_message(f"{member.username} покинул чат.", old_chat_id, member.client_socket,
                                          system_msg=True)
                    broadcast_message(f"{member.username} зашёл в чат.", member.chat_id, None, system_msg=True)
                    continue
                if member.username is None:
                    send_message(client_socket,
                                 "[SYSTEM] Чтобы присоединиться к чату, вам нужно установить никнейм. Введите /setup_nickname <ваш никнейм>")
                elif member.chat_id is None:
                    send_message(client_socket, "[SYSTEM] Вы не присоединились к чату. Введите /join_chat <чат_айди>")
                else:
                    broadcast_message(message, member.chat_id, client_socket)
            else:
                break
        except ConnectionResetError:
            break

    print(f"[-] Отключен {client_address}")
    member = find_chat_member(client_socket)
    if member.chat_id is not None:
        target_chat_id = member.chat_id
        members.remove(member)
        broadcast_message(f"{member.username} покинул чат.", target_chat_id, client_socket, system_msg=True)
    remove_chat_member(client_socket)
    client_socket.close()


def find_chat_member(target_socket) -> tp.Union[ChatMember, None]:
    for member in members:
        if member.client_socket == target_socket:
            return member
    return None


def remove_chat_member(target_socket):
    for member in members:
        if member.client_socket == target_socket:
            members.remove(member)
            break


def broadcast_message(message, chat_id, sender_socket, system_msg: bool = False):
    sender = find_chat_member(sender_socket)
    for member in members:
        if member.chat_id == chat_id:
            try:
                full_message = (
                                   "[SYSTEM]" if system_msg else f"[{sender.username}{' (You)' if member.client_socket == sender_socket else ''}]") + f" {message}"
                send_message(member.client_socket, full_message)
            except:
                member.client_socket.close()
                members.remove(member)
                broadcast_message(f"{member.username} покинул чат.", chat_id, client_socket, system_msg=True)


def send_message(client_socket, message):
    msg = message.encode('utf-8')
    msg_length = len(msg).to_bytes(BUFFER_SIZE, byteorder='big')
    client_socket.sendall(msg_length + msg)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[*] Сервер запущен на {HOST}:{PORT}")

while True:
    client_socket, client_address = server.accept()

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
