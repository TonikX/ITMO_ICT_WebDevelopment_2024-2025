import socket


def start_client():
    # Создаем TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Подключаемся к серверу
    server_address = ('localhost', 8080)
    client_socket.connect(server_address)

    try:
        # Ввод коэффициентов уравнения
        a = float(input("Введите коэффициент a: "))
        b = float(input("Введите коэффициент b: "))
        c = float(input("Введите коэффициент c: "))

        # Отправляем данные на сервер
        message = f"{a},{b},{c}"
        client_socket.sendall(message.encode())
        print(f"Отправлено уравнение с параметрами: a={a}, b={b}, c={c}")

        # Получаем ответ от сервера
        data = client_socket.recv(1024).decode()
        print(f"Результат от сервера: {data}")

    finally:
        # Закрываем сокет
        client_socket.close()


if __name__ == "__main__":
    start_client()
