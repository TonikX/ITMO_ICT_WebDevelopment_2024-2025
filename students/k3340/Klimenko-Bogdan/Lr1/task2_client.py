import socket

# Настройки сервера
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12346
BUFFER_SIZE = 1024

# Создаём TCP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Подключаемся к серверу
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Подключено к серверу.")

    # Ввод данных
    a = input("Введите длину первого основания (a): ")
    b = input("Введите длину второго основания (b): ")
    h = input("Введите высоту (h): ")

    # Формируем строку для отправки
    data = f"{a},{b},{h}"
    client_socket.send(data.encode('utf-8'))

    # Получаем ответ
    response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print("Ответ сервера:", response)

except ConnectionRefusedError:
    print("Ошибка: сервер не запущен или недоступен.")
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    client_socket.close()