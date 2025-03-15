# Лабораторная работа 1

Работа с с веб-сокетами

# Задание 1

## Цель

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. 
В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## Код клиента
    import socket
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345
    BUFFER_SIZE = 1024
    
    def udp_client():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            message = "Hello, server_bro"
            client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
            print(f"Сообщение отправлено серверу: {message}")
    
            response, _ = client_socket.recvfrom(BUFFER_SIZE)
            print(f"Ответ от сервера: {response.decode()}")

    if __name__ == "__main__":
        udp_client()

## Код сервера
    import socket
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345
    BUFFER_SIZE = 1024
    
    def udp_server():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((SERVER_HOST, SERVER_PORT))
            print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
    
            while True:
                message, client_address = server_socket.recvfrom(BUFFER_SIZE)
                print(f"Сообщение от клиента: {message.decode()}")
    
                response = "Hello, client_bro"
                server_socket.sendto(response.encode(), client_address)
                print(f"Ответ отправлен клиенту {client_address}")
    
    if __name__ == "__main__":
        udp_server()

# Задание 2

## Цель

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. 
Сервер обрабатывает данные и возвращает результат клиенту.

## Код клиента
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


## Код сервера
    import socket
    import math
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345
    BUFFER_SIZE = 1024
    
    
    def calculate(request):
        try:
            operation, *args = request.split(',')
            args = list(map(float, args))
    
            if operation == "1":  # Теорема Пифагора
                a, b = args
                result = math.sqrt(a ** 2 + b ** 2)
                return f"Гипотенуза: {result:.2f}"
    
            elif operation == "2":  # Решение квадратного уравнения
                a, b, c = args
                discriminant = b ** 2 - 4 * a * c
                if discriminant > 0:
                    x1 = (-b + math.sqrt(discriminant)) / (2 * a)
                    x2 = (-b - math.sqrt(discriminant)) / (2 * a)
                    return f"Корни уравнения: x1={x1:.2f}, x2={x2:.2f}"
                elif discriminant == 0:
                    x = -b / (2 * a)
                    return f"Единственный корень: x={x:.2f}"
                else:
                    return "Нет действительных корней"
    
            elif operation == "3":  # Площадь трапеции
                a, b, h = args
                result = ((a + b) / 2) * h
                return f"Площадь трапеции: {result:.2f}"
    
            elif operation == "4":  # Площадь параллелограмма
                base, height = args
                result = base * height
                return f"Площадь параллелограмма: {result:.2f}"
    
            else:
                return "Неизвестная операция"
        except (ValueError, IndexError):
            return "Ошибка обработки данных. Проверьте ввод."
    
    
    def tcp_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((SERVER_HOST, SERVER_PORT))
            server_socket.listen(1)
            print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
    
            while True:
                conn, addr = server_socket.accept()
                print(f"Подключение от клиента: {addr}")
                with conn:
                    while True:
                        data = conn.recv(BUFFER_SIZE)
                        if not data:
                            break
                        request = data.decode()
                        print(f"Получено сообщение: {request}")
    
                        response = calculate(request)
                        conn.sendall(response.encode())
    
    
    if __name__ == "__main__":
        tcp_server()

# Задание 3
## Цель
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Код HTML-страницы
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Привет, клиент!</title>
    </head>
    <body>
        <h1>Добро пожаловать на HTTP-сервер!</h1>
        <p>Этот сервер возвращает HTML-страницу из файла <strong>index.html</strong>.</p>
    </body>
    </html>


## Код сервера
    import socket
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080
    BUFFER_SIZE = 1024
    HTML_FILE = 'index.html'
    
    def load_html(file_path):
        """Загружает содержимое HTML-файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "<html><body><h1>404 Not Found</h1></body></html>"
    
    def tcp_server():
        """Запуск HTTP-сервера."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((SERVER_HOST, SERVER_PORT))
            server_socket.listen(1)
            print(f"HTTP-сервер запущен на http://{SERVER_HOST}:{SERVER_PORT}")
    
            while True:
                conn, addr = server_socket.accept()
                print(f"Подключение от клиента: {addr}")
                with conn:
                    request = conn.recv(BUFFER_SIZE).decode()
                    print(f"Запрос:\n{request}")
    
                    html_content = load_html(HTML_FILE)
    
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                        "\r\n"
                        f"{html_content}"
                    )
    
                    conn.sendall(response.encode())
                    print("Ответ отправлен клиенту.")
    
    if __name__ == "__main__":
        tcp_server()

# Задание 4

## Цель

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

## Код клиента
    import socket
    import threading
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345
    BUFFER_SIZE = 1024
    
    def receive_messages(client_socket):
        """Получает и выводит сообщения от сервера."""
        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE).decode()
                if not message:
                    break
                print(message)
            except ConnectionResetError:
                print("Соединение с сервером потеряно.")
                break
        client_socket.close()
    
    def tcp_client():
        """Запуск TCP-клиента."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("Подключено к серверу.")
    
            thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
            thread.start()
            
            while True:
                message = input()
                if message.lower() == "exit":
                    print("Отключение от сервера.")
                    break
                try:
                    client_socket.send(message.encode())
                except BrokenPipeError:
                    print("Соединение с сервером разорвано.")
                    break
    
    if __name__ == "__main__":
        tcp_client()

## Код сервера
    import socket
    import threading
    
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345
    BUFFER_SIZE = 1024
    
    
    clients = []
    
    def handle_client(client_socket, address):
        """Обрабатывает отдельного клиента."""
        print(f"Подключен клиент: {address}")
        clients.append(client_socket)
    
        try:
            while True:
                message = client_socket.recv(BUFFER_SIZE).decode()
                if not message:
                    break
                print(f"Сообщение от {address}: {message}")
    
                broadcast(message, client_socket)
        except ConnectionResetError:
            print(f"Клиент {address} отключился.")
        finally:
            clients.remove(client_socket)
            client_socket.close()
    
    def broadcast(message, sender_socket):
        """Рассылает сообщение всем клиентам, кроме отправителя."""
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except:
                    clients.remove(client)
    
    def tcp_server():
        """Запуск TCP-сервера."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((SERVER_HOST, SERVER_PORT))
            server_socket.listen()
            print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
    
            while True:
                client_socket, address = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
                thread.start()
    
    if __name__ == "__main__":
        tcp_server()

# Задание 5

## Цель
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.
Сервер должен:
Принять и записать информацию о дисциплине и оценке по дисциплине.
Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

## Код сервера
    import socket
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080
    BUFFER_SIZE = 1024
    
    
    grades = []
    
    def handle_get():
        """Обрабатывает GET-запрос и формирует HTML-страницу с оценками."""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Оценки</title>
        </head>
        <body>
            <h1>Список оценок</h1>
            <table border="1">
                <tr>
                    <th>Дисциплина</th>
                    <th>Оценка</th>
                </tr>
        """
        for discipline, grade in grades:
            html_content += f"""
                <tr>
                    <td>{discipline}</td>
                    <td>{grade}</td>
                </tr>
            """
        html_content += """
            </table>
            <form method="POST" action="/">
                <h2>Добавить оценку</h2>
                <label>Дисциплина: <input type="text" name="discipline"></label><br>
                <label>Оценка: <input type="text" name="grade"></label><br>
                <button type="submit">Добавить</button>
            </form>
        </body>
        </html>
        """
        return (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
            "\r\n"
            + html_content
        )
    
    def handle_post(request):
        """Обрабатывает POST-запрос и добавляет данные в хранилище."""
        body = request.split("\r\n\r\n", 1)[1]  # Получаем тело запроса
        params = dict(param.split("=") for param in body.split("&"))
        discipline = params.get("discipline", "").replace("+", " ")
        grade = params.get("grade", "").replace("+", " ")
        if discipline and grade:
            grades.append((discipline, grade))
        return (
            "HTTP/1.1 303 See Other\r\n"
            "Location: /\r\n"
            "\r\n"
        )
    
    def tcp_server():
        """Запуск веб-сервера."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((SERVER_HOST, SERVER_PORT))
            server_socket.listen(1)
            print(f"Сервер запущен на http://{SERVER_HOST}:{SERVER_PORT}")
    
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    request = conn.recv(BUFFER_SIZE).decode()
                    if not request:
                        continue
    
                    headers = request.split("\r\n")
                    method, path, _ = headers[0].split()
    
                    if method == "GET":
                        response = handle_get()
                    elif method == "POST":
                        response = handle_post(request)
                    else:
                        response = (
                            "HTTP/1.1 405 Method Not Allowed\r\n"
                            "Content-Length: 0\r\n"
                            "\r\n"
                        )
    
                    conn.sendall(response.encode())
    
    if __name__ == "__main__":
        tcp_server()

---

[Назад к главной странице](index.md)
