import socket
import threading

HOST = socket.gethostname()
PORT = 8000
MAX_CONNECTIONS = 10
CHAT_ID_SIZE = 1
MESSAGE_SIZE = 1024

type ChatId = str
type Socket = socket.socket
lock = threading.Lock()


class ChatConnectionManager:
    _chat_connections: dict[ChatId, list[Socket]]

    def __init__(self) -> None:
        self._chat_connections = dict()

    def connect_client_to_chat(self, chat_id: str, client: Socket) -> None:
        is_chat_exists = self._chat_connections.get(chat_id, None) is not None
        if not is_chat_exists:
            self._chat_connections[chat_id] = []

        self._chat_connections[chat_id].append(client)

    def disconnect_client_from_chat(self, chat_id: str, client: Socket) -> None:
        chat_connections = self._chat_connections.get(chat_id, None)
        if chat_connections is None:
            return

        chat_connections.remove(client)
        client.close()

    def send_message(self, chat_id: str, message: str) -> None:
        chat_connections = self._chat_connections.get(chat_id, None)
        if chat_connections is None:
            return

        for client_socket in chat_connections:
            client_socket.send(message.encode())


chat_connection_manager = ChatConnectionManager()


def consume_client(client: Socket) -> None:
    chat_id = client.recv(CHAT_ID_SIZE).decode()
    with lock:
        chat_connection_manager.connect_client_to_chat(chat_id, client)

    while True:
        message = client.recv(MESSAGE_SIZE).decode()
        if message == "exit":
            chat_connection_manager.disconnect_client_from_chat(chat_id, client)
            break

        chat_connection_manager.send_message(chat_id=chat_id, message=message)


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    while True:
        client, _ = server.accept()
        thread = threading.Thread(
            target=consume_client,
            args=(client,),
        )

        thread.start()

    server.close()


if __name__ == "__main__":
    serve()
