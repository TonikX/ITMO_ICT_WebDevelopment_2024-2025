import socket
def get_positive_number(numb):
    while True:
        try:
            value = float(input(numb))
            if value > 0:
                return value
            else:
                print("Ошибка: значение должно быть положительным.")
        except ValueError:
            print("Ошибка: введено неверное число.")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12346))
    a = get_positive_number("Введите длину первого катета: ")
    b = get_positive_number("Введите длину второго катета: ")
    data = f"{a},{b}"
    client_socket.sendall(data.encode())
    result = client_socket.recv(1024).decode()
    print(f"Гипотенуза: {result}")
    client_socket.close()

if __name__ == '__main__':
    start_client()