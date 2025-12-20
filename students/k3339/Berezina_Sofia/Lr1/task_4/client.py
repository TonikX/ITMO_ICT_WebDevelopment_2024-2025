import socket
import threading
import sys

def client_program():
    sock = socket.socket()
    try:
        sock.connect(('127.0.0.1', 14901))
        print("Успешно подключились к серверу")
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу")
        return

    def recv_msg():
        while True:
            try:
                msg = sock.recv(1000).decode('utf-8')
                if not msg:
                    print("Сервер отключен")
                    sys.exit(0)
                if msg == 'nickname':
                    print("Введите ваш никнейм: ", end='', flush=True)
                else:
                    print(msg)
            except (ConnectionResetError, OSError):
                print("\nСоединение с сервером разорвано")
                sys.exit(0)
            except Exception:
                sys.exit(0)

    # Запускаем поток для приема сообщений
    recv_thread = threading.Thread(target=recv_msg)
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while True:
            try:
                msg = input()
                sock.send(msg.encode('utf-8'))
            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Соединение с сервером потеряно")
                break
            except KeyboardInterrupt:
                print("\nЗавершение работы")
                break
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\nЗавершение работы")
    finally:
        sock.close()

if __name__ == "__main__":
    client_program()