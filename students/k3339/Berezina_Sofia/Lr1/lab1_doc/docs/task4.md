# Задание № 4. Реализация многопользовательского чата

## Задача
Мне предстояло создать многопользовательский чат с использованием TCP-протокола. Основная сложность заключалась в организации одновременной работы нескольких клиентов и корректной маршрутизации сообщений между ними.

### 1. Реализация серверной части

Сервер я начала с создания TCP-сокета и привязки его к localhost на порту 14901. Использовала бесконечный цикл для постоянного принятия новых подключений. При подключении каждого клиента сервер сразу запрашивает никнейм, отправляя специальное сообщение "nickname".

Для хранения информации о клиентах создала два списка: clients (для сокетов) и nicknames (для ников). Это позволяет сопоставлять каждому соединению соответствующий никнейм.

Самым сложным было организовать обработку сообщений от каждого клиента в отдельных потоках. Для этого создала функцию handle_client, которая в бесконечном цикле принимает сообщения от конкретного клиента и рассылает их всем остальным участникам чата, добавляя имя отправителя.

Важной задачей была обработка отключений клиентов. При возникновении ошибки чтения сообщения сервер удаляет клиента из списков и корректно завершает поток.

```python
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
```

### 2. Реализация клиентской части

Клиентская часть начинается с подключения к серверу. Я организовала два параллельных процесса: прием сообщений в отдельном потоке и отправка сообщений в основном потоке.

Для приема сообщений создала функцию recv_msg, которая постоянно ожидает данные от сервера. При получении специального запроса "nickname" клиент запрашивает у пользователя ввод никнейма и отправляет его на сервер. Все остальные сообщения просто выводятся на экран.

Основной цикл клиента отвечает за ввод сообщений с клавиатуры и их отправку на сервер. Простота этой части компенсируется сложностью многопоточной организации приема сообщений.

Самым интересным моментом было тестирование чата с несколькими подключениями. Я запускала несколько экземпляров клиента и наблюдала, как сообщения корректно доставляются всем участникам. Особенно приятно было видеть, что никнеймы правильно отображаются у всех пользователей.

```python
import socket
import threading
import sys

def client_program():
    sock = socket.socket()
    try:
        sock.connect(('127.0.0.1', 14901))
        print("Успешно подключились к серверу")
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу")
        return

    def recv_msg():
        while True:
            try:
                msg = sock.recv(1000).decode('utf-8')
                if not msg:
                    print("Сервер отключен")
                    sys.exit(0)
                if msg == 'nickname':
                    print("Введите ваш никнейм: ", end='', flush=True)
                else:
                    print(msg)
            except (ConnectionResetError, OSError):
                print("\nСоединение с сервером разорвано")
                sys.exit(0)
            except Exception:
                sys.exit(0)

    # Запускаем поток для приема сообщений
    recv_thread = threading.Thread(target=recv_msg)
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while True:
            try:
                msg = input()
                sock.send(msg.encode('utf-8'))
            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Соединение с сервером потеряно")
                break
            except KeyboardInterrupt:
                print("\nЗавершение работы")
                break
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\nЗавершение работы")
    finally:
        sock.close()

if __name__ == "__main__":
    client_program()
```