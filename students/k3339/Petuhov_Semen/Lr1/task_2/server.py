import socket
import math

#Обработчик необходимых математических операций
def math_operation(operation, params):
    if operation == '1':  # Пифагор
        a, b = float(params[0]), float(params[1])
        return math.sqrt(a * a + b * b)

    elif operation == '2':  # Квадратное уравнение
        a, b, c = float(params[0]), float(params[1]), float(params[2])
        discrim = b ** 2 - 4 * a * c
        if discrim > 0:
            x1 = (-b + math.sqrt(discrim)) / (2 * a)
            x2 = (-b - math.sqrt(discrim)) / (2 * a)
            return x1, x2
        elif discrim == 0:
            x1 = -b / (2 * a)
            return x1
        else:
            return "Уравнение не имеет действительных корней"

    elif operation == '3':  # Площадь трапеции
        a, b, h = float(params[0]), float(params[1]), float(params[2])
        return (a + b) / 2 * h

    elif operation == '4':  # Площадь параллелограмма
        base, height = float(params[0]), float(params[1])
        return base * height

    else:
        return "Неверный номер операции"

#Создание сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 1934)
server_socket.bind(server_address)
server_socket.listen(1)
#Обработчик сообщений
while True:
    connection, client_address = server_socket.accept() #Подключение клиента
    try:
        print(f"Client_address: {client_address}")
        #Обработчик сообщения от пользователя
        data = connection.recv(1024).decode()
        if data:
            parts = data.split(' ')
            operation = parts[0]
            params = parts[1:]

            result = math_operation(operation, params)

            connection.sendall(str(result).encode())
        else:
            break
    finally:
        connection.close()