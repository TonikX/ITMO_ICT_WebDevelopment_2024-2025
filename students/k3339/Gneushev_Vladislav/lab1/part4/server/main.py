import constants
from connection_manager import ConnectionManager
from server import Server
from logs import setup_logging


def main():
    setup_logging()

    server = Server(
        host=constants.SERVER_HOST,
        port=constants.SERVER_PORT,
        connection_manager=ConnectionManager()
    )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
