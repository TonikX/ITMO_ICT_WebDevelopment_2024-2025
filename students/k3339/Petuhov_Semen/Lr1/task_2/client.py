import socket

#Логика консольного ввода
def get_operation_inp():
    print("Выберите операцию:")
    print("1. Теорема Пифагора")
    print("2. Решение квадратного уравнения")
    print("3. Площадь трапеции")
    print("4. Площадь параллелограмма")

    operation = input("Введите номер операции: ")

    if operation == '1':
        a = int(input("Введите сторону a: "))
        b = int(input("Введите сторону b: "))
        return f"1 {a} {b}"

    elif operation == '2':
        a = int(input("Введите коэффициент a: "))
        b = int(input("Введите коэффициент b: "))
        c = int(input("Введите коэффициент c: "))
        return f"2 {a} {b} {c}"

    elif operation == '3':
        a = int(input("Введите основание a: "))
        b = int(input("Введите основание b: "))
        h = int(input("Введите высоту h: "))
        return f"3 {a} {b} {h}"

    elif operation == '4':
        base = int(input("Введите основание: "))
        height = int(input("Введите высоту: "))
        return f"4 {base} {height}"
    else:
        return "Неверный номер операции"

#Подключение сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 1934)
client_socket.connect(server_address)
#Отправка запроса
try:
    request = get_operation_inp()
    client_socket.sendall(request.encode())
    data = client_socket.recv(1024)
    print("Результат выполнения операции:", data.decode())

finally:
    client_socket.close()