import socket
import threading


class ChatServer:
    def __init__(self, host: str, port: int, max_clients: int = 10):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.bind((host, port))
        self._conn.listen(max_clients)
        self._conn.settimeout(1)

        self._is_running = True
        self._lock = threading.Lock()
        self._clients = []

    def _broadcast(self, message: str, sender_client: socket.socket) -> None:
        for client in self._clients:
            if client == sender_client:
                continue

            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Не получилось отправить сообщение клиенту {client.getpeername()}: {e}")

    def _handle_client(self, client_socket: socket.socket) -> None:
        with self._lock:
            self._clients.append(client_socket)
        
        client_name = client_socket.getpeername()
        message = f"Клиент {client_name} подключился"
        
        self._broadcast(message=message, sender_client=client_socket )
        print(message)

        while self._is_running:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break

                print(f"Получено сообщение от {client_name}: {message}")

                self._broadcast(
                    message=f"{client_name}: {message}",
                    sender_client=client_socket,
                )
            except Exception as e:
                print(f"Ошибка при работе с клиентом {client_name}: {e}")
                break

        self._remove_client(client_socket)

    def _remove_client(self, client_socket: socket.socket):
        with self._lock:
            if client_socket in self._clients:
                self._clients.remove(client_socket)

                message = f"{client_socket.getpeername()} покинул чат"
                self._broadcast(message=message, sender_client=client_socket)
                print(message)

                client_socket.close()

    def _shutdown(self):
        self._is_running = False

        for client in self._clients:
            try:
                client.send("Сервер завершил работу".encode())
                client.close()
            except Exception as e:
                print(f"Ошибка во время отключения клиента: {e}")

        self._conn.close()
        print("Сервер успешно остановлен")

    def serve(self):
        while self._is_running:
            try:
                client_socket, _ = self._conn.accept()
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
                client_thread.start()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                self._shutdown()
                break

def main():
    chat_server = ChatServer(host="localhost", port=12345)
    try:
        chat_server.serve()
    except KeyboardInterrupt:
        print("Сервер остановлен")


if __name__ == "__main__":
    main()

