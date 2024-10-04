import socket
import threading

users = []


def send_msg(message, user_socket):
    for user in users:
        if user != user_socket:
            try:
                user.send(message)
            except:
                user.remove(users)


def handle_message(user_socket, user_address):
    print(f"User is connected: {user_address}")
    users.append(user_socket)
    while True:
        try:
            message = user_socket.recv(1024)
            if message.decode() == "leave":
                users.remove(user_socket)
                user_socket.close()
            else:
                print(f"Message received from {user_address}: {message.decode()}")
                send_msg(message, user_socket)
        except:
            break
    print(f"User disconnected: {user_address}")
    users.remove(user_socket)
    user_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("Сервер запущен и ждет подключений...")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_message, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    start_server()