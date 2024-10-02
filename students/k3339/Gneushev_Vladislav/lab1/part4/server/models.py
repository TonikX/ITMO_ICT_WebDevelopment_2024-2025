from dataclasses import dataclass
from socket import socket


@dataclass
class Connection:
    sock: socket
    address: tuple[str, int]
    user_name: str | None = None

    def receive_message(self) -> str | None:
        try:
            data = self.sock.recv(1024)
            udata = data.decode("utf-8")
            if not udata:
                return None
            return udata
        except socket.timeout:
            return None

    def send_message(self, message: str):
        self.sock.send(message.encode("utf-8"))

    def close(self):
        self.sock.close()

    def set_timeout(self, timeout: float):
        self.sock.settimeout(timeout)

    def __str__(self) -> str:
        return f"{self.address[0]}:{self.address[1]}"
