import socket
import threading

# Хранение подключённых клиентов и их никнеймов
clients = {}


def broadcast(message: str, sender_socket: socket.socket | None = None):
    """
    Рассылает сообщение всем клиентам, кроме отправителя (если указан).
    """
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                # Удаляем клиента при ошибке отправки
                client_socket.close()
                del clients[client_socket]


def handle_client(client_socket: socket.socket, client_address) -> None:
    """
    Обрабатывает одного клиента: получает его никнейм и сообщения.
    """
    print(f'Клиент подключён: {client_address}')
    client_socket.send('Введите ваш никнейм: '.encode())

    try:
        nickname = client_socket.recv(1024).decode().strip()
        if not nickname:
            client_socket.send('Никнейм не может быть пустым. Отключение.\n'.encode())
            client_socket.close()
            return
        clients[client_socket] = nickname
        print(f'Никнейм клиента: {nickname}')
        broadcast(f'{nickname} присоединился к чату!\n')

        # Отправляем приветственное сообщение
        client_socket.send(f'Server: Добро пожаловать в чат, {nickname}! Вы можете отправлять сообщения.\n'.encode())

        # Приём сообщений от клиента
        while True:
            message = client_socket.recv(1024)
            if not message:
                break  # Клиент отключился

            # Рассылаем сообщение всем
            broadcast(f'{nickname}: {message.decode()}', sender_socket=client_socket)

    except Exception as e:
        print(f'Соединение с клиентом {client_address} потеряно из-за ошибки:\n{e}')
    finally:
        # Удаляем клиента при отключении
        print(f'Клиент {nickname} ({client_address}) отключился.')
        broadcast(f'{nickname} покинул чат.')
        del clients[client_socket]
        client_socket.close()


def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print('Сервер запущен и ожидает подключения клиентов...')

    while True:
        # Принимаем новое подключение
        client_socket, client_address = server_socket.accept()

        # Запускаем поток для обработки клиента
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == '__main__':
    start_server()
