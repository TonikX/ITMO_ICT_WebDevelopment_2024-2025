import socket
import threading
#Массив с текущими пользователями
users = []

#Отправка сообщений всем пользователям, кроме отправителя
def send_msg(message, user_socket):
    for user in users:
        if user != user_socket:
            try:
                print(message)
                user.send(message)
            except:
                user.remove(users)

#Функция для обработки сообщений(запускается в потоке индивидуально для каждого клиента)
def handle_message(user_socket, user_address):
    #Подключение пользователя
    print(f"User is connected: {user_address}")
    users.append(user_socket)
    #Обработка сообщений
    while True:
        try:
            message = user_socket.recv(1024)
            if message.decode() == "/leave":
                users.remove(user_socket)
                user_socket.close()
            else:
                print(f"Message received from {user_address}: {message.decode()}")
                msg_with_addr = str(user_address[1])+ ": " + message.decode()
                send_msg(msg_with_addr.encode(), user_socket)
        except:
            break
    print(f"User disconnected: {user_address}")
    users.remove(user_socket)
    user_socket.close()

#Запуск сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("Сервер запущен")

    while True:
        client_socket, client_address = server_socket.accept()
        #Реализация потоков
        thread = threading.Thread(target=handle_message, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    start_server()