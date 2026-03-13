import socket
import threading

# Настройки сервера
HOST = '127.0.0.1'
PORT = 12347

# Список подключенных клиентов: каждый элемент - кортеж (сокет, имя)
clients = []

def broadcast(message, sender_socket=None):
    """
    Отправляет сообщение всем клиентам, кроме отправителя.
    Если sender_socket = None, сообщение отправляется всем.
    """
    for client_socket, _ in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                # Если клиент отключился, удалим его при следующей итерации
                pass

def handle_client(client_socket, addr):
    """
    Функция для обработки одного клиента в отдельном потоке.
    """
    # Запрашиваем имя у клиента
    try:
        client_socket.send("Введите ваше имя: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8').strip()
        if not name:
            name = f"User{addr[1]}"  # если имя пустое, генерируем
    except:
        # Если не удалось получить имя, закрываем соединение
        client_socket.close()
        return

    # Добавляем клиента в список
    clients.append((client_socket, name))
    print(f"Новый клиент: {name} ({addr})")
    broadcast(f"{name} присоединился к чату!", client_socket)

    try:
        while True:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # Если recv вернул пустую строку, клиент отключился
                break
            print(f"Сообщение от {name}: {message}")
            broadcast(f"{name}: {message}", client_socket)
    except:
        # Любая ошибка (например, разрыв соединения) приводит к выходу из цикла
        pass
    finally:
        # Удаляем клиента из списка
        clients[:] = [c for c in clients if c[0] != client_socket]
        client_socket.close()
        print(f"{name} отключился.")
        broadcast(f"{name} покинул чат.", None)

# Создаём серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # чтобы быстро переиспользовать порт
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Чат-сервер запущен на {HOST}:{PORT}")

try:
    while True:
        client_socket, addr = server_socket.accept()
        # Создаём поток для нового клиента
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.daemon = True  # поток завершится при завершении основного потока
        thread.start()
except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()