import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 8080

def receive_loop(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print(f"\n[SERVER] соединение закрыто")
                break
            print(data.decode("utf-8"), end="")
        except OSError:
            break
    sys.exit(0)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    name = input("Ваше имя: ").strip() or "anon"
    sock.sendall((name + '\n').encode("utf-8"))

    t = threading.Thread(
        target=receive_loop,
        args=(sock,),
        daemon=True
    )
    t.start()

    print(f"Введите сообщение ( или /quit для выхода или /users для списка):")
    try:
        while True:
            msg = input()
            if not msg:
                continue
            sock.sendall((msg + '\n').encode("utf-8"))
            if msg == "/quit":
                break
    except (KeyboardInterrupt, OSError):
        pass
    finally:
        sock.close()
        print("Вы вышли из чата(")

if __name__ == "__main__":
    main()



