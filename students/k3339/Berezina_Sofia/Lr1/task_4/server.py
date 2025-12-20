import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 14901))
server.listen()

clients, nicknames = [], []
clients_lock = threading.Lock()

print("Сервер чата запущен")


def handle_client(client):
    # Получаем никнейм клиента
    with clients_lock:
        index = clients.index(client)
        nickname = nicknames[index]

    while True:
        try:
            msg = client.recv(1000).decode('utf-8')
            if not msg:  # Клиент отключился
                break

            # Рассылаем сообщение всем клиентам
            with clients_lock:
                # Создаем копию списка для безопасной итерации
                clients_copy = clients.copy()

            for c in clients_copy:
                if c != client:
                    try:
                        c.send(f"{nickname}: {msg}".encode('utf-8'))
                    except:
                        # Если отправка не удалась, клиент будет удален позже
                        pass

        except:
            break

    # Удаляем клиента после отключения
    with clients_lock:
        if client in clients:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames.pop(index)
            print(f"{nickname} покинул чат")

    client.close()


try:
    while True:
        client, addr = server.accept()

        try:
            client.send("nickname".encode('utf-8'))
            nickname = client.recv(1000).decode('utf-8')

            with clients_lock:
                nicknames.append(nickname)
                clients.append(client)

            print(f"Новый участник чата {nickname}")

            # Запускаем поток для обработки клиента
            client_thread = threading.Thread(target=handle_client, args=(client,))
            client_thread.daemon = True
            client_thread.start()

        except Exception as e:
            print(f"Ошибка при подключении клиента: {e}")
            client.close()

except KeyboardInterrupt:
    print("\nЗавершение работы сервера")
finally:
    # Закрываем все соединения
    with clients_lock:
        for client in clients:
            try:
                client.close()
            except:
                pass
    server.close()