import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 65432))
    try:
        a = float(input("Введите длину первого катета: "))
        b = float(input("Введите длину второго катета: "))
        # Отправляем данные на сервер
        client_socket.send(f"{a},{b}".encode())

        # Получаем результат от сервера
        result = client_socket.recv(1024).decode()
        print(f"Результат от сервера: {result}")
    except ValueError:
        print("Ошибка: введены некорректные данные.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()