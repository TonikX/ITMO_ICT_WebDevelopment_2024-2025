import socket
import threading

HOST = '127.0.0.1'
PORT = 8080


def receive_messages(server):
    while True:
        try:
            data = server.recv(1024).decode()
            if not data:
                print("[SERVER DISCONNECTED]")
                break
            print(data)
        except Exception as e:
            print(f"[ERROR] Ошибка при получении сообщения: {e}")
            break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"[CONNECTED] Подключено к {HOST}:{PORT}")

            threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

            while True:
                message = input()
                if message.lower() == 'exit':
                    print("[DISCONNECTED] Отключение от сервера...")
                    break
                s.send(message.encode())
        except ConnectionRefusedError:
            print("[ERROR] Не удалось подключиться к серверу. Убедитесь, что он запущен.")
        except Exception as e:
            print(f"[ERROR] Ошибка: {e}")

if __name__ == "__main__":
    main()