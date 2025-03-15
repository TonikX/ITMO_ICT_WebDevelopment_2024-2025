import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Подключено к серверу.")

        while True:
            print("\nВыберите операцию:")
            print("1: Теорема Пифагора (a, b)")
            print("2: Решение квадратного уравнения (a, b, c)")
            print("3: Площадь трапеции (a, b, h)")
            print("4: Площадь параллелограмма (base, height)")
            print("0: Выход")

            operation = input("Введите номер операции: ")
            if operation == "0":
                print("Выход из программы.")
                break

            if operation in ["1", "2", "3", "4"]:
                args = input("Введите параметры через запятую: ")
                request = f"{operation},{args}"
                client_socket.sendall(request.encode())

                response = client_socket.recv(1024)
                print(f"Ответ сервера: {response.decode()}")
            else:
                print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    tcp_client()
