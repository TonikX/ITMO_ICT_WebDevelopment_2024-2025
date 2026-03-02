import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000
BUFFER_SIZE = 1024

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "Hello, server"
    sock.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))
    print(f"Отправлено на сервер: {message}")

    data, addr = sock.recvfrom(BUFFER_SIZE)
    reply = data.decode("utf-8")
    print(f"Ответ от сервера: {reply}")

    sock.close()

if __name__ == "__main__":
    main()
