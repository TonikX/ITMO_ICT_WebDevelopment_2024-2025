import socket

def start_client():
    socket_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_user.connect(('localhost', 8090))  # Подключаемся к серверу на localhost:9999

    # Вводим два числа
    a = input("Введите a: ")
    b = input("Введите b: ")

    # Отправляем данные на сервер
    socket_user.send(f"{a} {b}".encode('utf-8'))

    # Получаем и выводим результат от сервера
    response = socket_user.recv(1024).decode('utf-8')
    print(f"Ответ: {response}")

    socket_user.close()

if __name__ == "__main__":
    start_client()
