import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000
BUFFER_SIZE = 1024

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"UDP-сервер запущен на {SERVER_IP}:{SERVER_PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode("utf-8")
        print(f"Получено от {addr}: {message}")

        reply = "Hello, client"
        sock.sendto(reply.encode("utf-8"), addr)
        print(f"Отправлено клиенту {addr}: {reply}")

if __name__ == "__main__":
    main()
