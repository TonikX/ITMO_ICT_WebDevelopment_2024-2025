import socket
import math

HOST = "127.0.0.1"
PORT = 13000
BUFFER_SIZE = 1024

def handle_request(data: str) -> str:
    # Ожидаем строку вида: a b
    # Возвращаем строку с результатом или ошибкой.
    try:
        parts = data.strip().split()
        if len(parts) != 2:
            return "Ошибка: введите два числа через пробел.\n"

        a = float(parts[0])
        b = float(parts[1])
        c = math.sqrt(a * a + b * b)
        return f"Результат: c = {c}\n"
    except ValueError:
        return "Ошибка: некорректные числа.\n"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"TCP-сервер (Пифагор) запущен на {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            print(f"Клиент подключился: {addr}")

            with conn:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        print(f"Клиент отключился: {addr}")
                        break

                    request = data.decode("utf-8")
                    print(f"Запрос от {addr}: {request!r}")

                    response = handle_request(request)
                    conn.sendall(response.encode("utf-8"))

if __name__ == "__main__":
    main()
