import socket
import threading

SERVER_ADDR = ("localhost", 9090)

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_addr):
        self.sock.connect(server_addr)

        stop_event = threading.Event()
        receive_thread = threading.Thread(
            target=self.receive_messages, args=(stop_event,), daemon=True
        )
        receive_thread.start()

        try:
            while not stop_event.is_set():
                message = input()
                if not message: continue
                try: self.sock.sendall(message.encode('utf-8'))
                except OSError: break

                if message.strip().lower() == '/exit': break
        except (KeyboardInterrupt, EOFError): pass
        finally:
            stop_event.set()
            self.sock.close()

    def receive_messages(self, stop_event):
        while not stop_event.is_set():
            try:
                data = self.sock.recv(1024)
                if not data:
                    stop_event.set()
                    break
                print(data.decode('utf-8'))
            except OSError:
                stop_event.set()
                break


if __name__ == "__main__":
    client = Client()
    try: client.connect(SERVER_ADDR)
    except ConnectionRefusedError:
        print("Server unavailable.")


