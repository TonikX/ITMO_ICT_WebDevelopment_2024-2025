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
