from models import Connection


class ConnectionManager:
    def __init__(self):
        self.connections: list[Connection] = []

    def add_connection(self, connection: Connection):
        # connection.set_timeout(1.0)
        self.connections.append(connection)

    def broadcast_message(
            self,
            message: str,
            exclude_nonames: bool = False
    ):
        for connection in self.connections:
            if exclude_nonames and connection.user_name is None:
                continue
            connection.send_message(message)

    def close_all_connections(self):
        for connection in self.connections:
            connection.close()
        self.connections.clear()

    def remove_connection(self, connection: Connection):
        if connection in self.connections:
            self.connections.remove(connection)
