import socket


def ask_square():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("127.0.0.1", 14900))

    params = get_params()
    conn.send(params.encode())

    result = conn.recv(1024).decode()
    print(f"Площадь параллелограмма: {result}")

    conn.close()


def get_params():
    a = input("Введите длину основания (a): ")
    h = input("Введите длину высоты (h): ")
    return f"{a} {h}"


if __name__ == "__main__":
    ask_square()
