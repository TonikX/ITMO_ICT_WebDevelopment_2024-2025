import socket
import threading


def broadcast_message(message, current_client):
    """
    Sending messages to all clients
    :param message: text of message
    :param current_client: current client info
    """
    for client in connected_clients:
        if client != current_client:
            try:
                client.send(message)
            except:
                client.close()
                remove_client(client)


def handle_client_connection(client_socket):
    """
    client connections handler
    :param client_socket:
    """
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Получено сообщение от клиента: {message.decode('utf-8')}")
                broadcast_message(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue


def remove_client(client_socket):
    if client_socket in connected_clients:
        connected_clients.remove(client_socket)


def start_server(host='127.0.0.1', port=8088):
    """
    server starter and worker
    :param host:
    :param port:
    :return:
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
        print(f"Сервер запущен на порту {port}")
        server_socket.listen()
        print("Ожидание подключений...")
    except Exception as error:
        print(f"Ошибка запуска сервера: {error}")
        return

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Подключён клиент с адреса: {client_address}")
            connected_clients.append(client_socket)
            threading.Thread(target=handle_client_connection, args=(client_socket,)).start()
        except Exception as error:
            print(f"Ошибка при подключении клиента: {error}")


if __name__ == "__main__":
    connected_clients = []
    start_server()
