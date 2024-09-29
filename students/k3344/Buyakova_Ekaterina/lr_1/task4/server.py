import socket
import threading

# Параметры сервера
HOST = 'localhost'
PORT = 8080

# Список для хранения подключенных клиентов
clients_list = []
client_id = 0  # Переменная для нумерации клиентов


# Функция для рассылки сообщений всем клиентам, кроме отправителя
def broadcast_message(message, current_client):
    for client in clients_list:
        if client['socket'] != current_client:
            try:
                client['socket'].send(message)
            except:
                # Если клиент отключился, то закрываем соединение
                client['socket'].close()
                clients_list.remove(client)


# Функция для обработки каждого клиента
def client_handling(client_socket, client_number):
    while True:
        try:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024)
            if message:
                decoded_message = message.decode('utf-8')
                print(f"Message from client {client_number}: {decoded_message}")

                # Формируем сообщение с номером клиента
                message_to_send = f"Client {client_number}: {decoded_message}".encode('utf-8')

                # Рассылаем сообщение всем клиентам, кроме отправителя
                broadcast_message(message_to_send, client_socket)
        except:
            # Закрываем соединение, если клиент отключился
            print(f"Client {client_number} is disconnected")
            client_socket.close()
            clients_list.remove({'socket': client_socket, 'id': client_number})
            break


# Запуск сервера
def server_starting():
    global client_id
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server starts on {HOST}:{PORT}")

    while True:
        # Принимаем новое соединение
        client_socket, client_address = server_socket.accept()
        client_id += 1
        print(f"New connection from client {client_address}. The client is assigned number {client_id}")

        # Добавляем клиента в список
        clients_list.append({'socket': client_socket, 'id': client_id})

        # Создаем отдельный поток для каждого клиента
        thread = threading.Thread(target=client_handling, args=(client_socket, client_id))
        thread.start()


# Запуск сервера
server_starting()
