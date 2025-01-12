# Task 4

Реализовать двухпользовательский или многопользовательский чат. Реализация
многопользовательского часа позволяет получить максимальное количество
баллов.
Реализовать с помощью протокола TCP – 100% баллов, с помощью UDP – 80%.

Обязательно использовать библиотеку threading.
Для реализации с помощью UDP, thearding использовать для получения
сообщений у клиента.

Для применения с TCP необходимо запускать клиентские подключения И прием
и отправку сообщений всем юзерам на сервере в потоках. Не забудьте сохранять юзеров,
чтобы потом отправлять им сообщения.

server.py
```python
import socket
import threading

HOST = '127.0.0.1'
PORT = 8080

clients = {}
addresses = {}


def handle_client(client_socket, client_address):
    try:
        name = client_socket.recv(1024).decode()
        welcome_message = f"{name} присоединился к чату."
        broadcast(bytes(welcome_message, "utf-8"))
        clients[client_socket] = name
        addresses[client_socket] = client_address

        while True:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, f"{name}: ")
            else:
                remove(client_socket)
                break
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке клиента {client_address}: {e}")
        remove(client_socket)


def broadcast(message, prefix=""):
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf-8") + message)
        except Exception as e:
            print(f"[ERROR] Не удалось отправить сообщение: {e}")


def remove(client_socket):
    name = clients[client_socket]
    del clients[client_socket]
    del addresses[client_socket]
    leave_message = f"{name} покинул чат."
    broadcast(bytes(leave_message, "utf-8"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Сервер запущен на порту", PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент {client_address}")
            client_socket.send(bytes("Введите ваше имя: ", "utf-8"))
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    main()

```
client1.py (аналогично client2.py и client3.py)
```python
import socket
import threading

HOST = '127.0.0.1'
PORT = 8080


def receive_messages(server):
    while True:
        try:
            data = server.recv(1024).decode()
            if not data:
                print("[SERVER DISCONNECTED]")
                break
            print(data)
        except Exception as e:
            print(f"[ERROR] Ошибка при получении сообщения: {e}")
            break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"[CONNECTED] Подключено к {HOST}:{PORT}")

            threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

            while True:
                message = input()
                if message.lower() == 'exit':
                    print("[DISCONNECTED] Отключение от сервера...")
                    break
                s.send(message.encode())
        except ConnectionRefusedError:
            print("[ERROR] Не удалось подключиться к серверу. Убедитесь, что он запущен.")
        except Exception as e:
            print(f"[ERROR] Ошибка: {e}")

if __name__ == "__main__":
    main()
```
