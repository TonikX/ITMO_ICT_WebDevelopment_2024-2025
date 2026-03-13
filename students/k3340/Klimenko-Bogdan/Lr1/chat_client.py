import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12347

def receive_messages(sock):
    """Поток для получения сообщений от сервера (запускается после ввода имени)."""
    try:
        while True:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            # Выводим сообщение и затем приглашение для ввода
            sys.stdout.write(f"\n{message}\n")
            sys.stdout.write("Вы: ")
            sys.stdout.flush()
    except:
        pass
    finally:
        print("\nСоединение с сервером потеряно.")
        sock.close()

# Подключаемся к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER_HOST, SERVER_PORT))
except ConnectionRefusedError:
    print("Ошибка: сервер не запущен. Запустите сервер и повторите попытку.")
    sys.exit(1)
try:
    prompt = client.recv(1024).decode('utf-8')
    print(prompt, end="")          # выводим "Введите ваше имя: "
    name = input()                  # вводим имя
    client.send(name.encode('utf-8'))
except:
    print("Ошибка при вводе имени.")
    client.close()
    sys.exit(1)

# Теперь запускаем поток для получения сообщений
recv_thread = threading.Thread(target=receive_messages, args=(client,))
recv_thread.daemon = True
recv_thread.start()

print("Добро пожаловать в чат! Для выхода введите '/exit'.")

# Основной цикл отправки сообщений
while True:
    try:
        msg = input("Вы: ")
        if msg.lower() == '/exit':
            break
        client.send(msg.encode('utf-8'))
    except KeyboardInterrupt:
        break
    except:
        print("Ошибка отправки.")
        break

client.close()