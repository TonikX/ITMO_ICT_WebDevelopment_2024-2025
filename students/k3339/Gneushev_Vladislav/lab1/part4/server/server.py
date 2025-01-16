import logging
import threading
from socket import socket, AF_INET, SOCK_STREAM

from connection_manager import ConnectionManager
from models import Connection

logger = logging.getLogger(__name__)


class Server:
    def __init__(
            self,
            host: str,
            port: int,
            connection_manager: ConnectionManager,
    ):
        self.host = host
        self.port = port
        self.connection_manager = connection_manager
        self.server_socket = socket(AF_INET, SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        logger.info(f"Server started on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            connection = Connection(sock=conn, address=addr)
            self.connection_manager.add_connection(connection)
            logger.info(f"Accepted connection from {addr}")

            threading.Thread(target=self._handle_client, args=(connection,)).start()

    def _handle_client(self, connection: Connection):
        with connection.sock:
            while True:
                try:
                    message = connection.receive_message()
                    if message is None:
                        break
                    self._handle_message(message, connection)
                except Exception as e:
                    self.connection_manager.remove_connection(connection)

    def _handle_message(self, message: str, connection: Connection):
        if connection.user_name is None:
            connection.user_name = message
            logger.info(f"connection [{connection}]: set username - {message}")
            return

        logger.info(f"Received message: {message} from {connection}")
        self.connection_manager.broadcast_message(
            f"[{connection.user_name}]: {message}",
            exclude_nonames=True
        )

    def stop(self):
        self.connection_manager.close_all_connections()
        self.server_socket.close()
        logger.info("Server stopped")
