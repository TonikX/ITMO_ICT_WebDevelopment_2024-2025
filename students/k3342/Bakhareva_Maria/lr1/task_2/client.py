import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

try:
    # Запрашиваем параметры у пользователя
    a = float(input("Введите коэффициент a: "))
    b = float(input("Введите коэффициент b: "))
    c = float(input("Введите коэффициент c: "))

    # Отправляем данные серверу
    client_socket.send(f"{a} {b} {c}".encode())

    # Получаем результат от сервера
    result = client_socket.recv(1024).decode()
    print(f"Результат: {result}")
except KeyboardInterrupt:
    print("\nКлиент остановлен.")
except Exception as e:
    print(f"Ошибка: {str(e)}")
finally:
    client_socket.close()
