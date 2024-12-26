import socket  # Импорт модуля для работы с сетевыми сокетами
import os  # Импорт модуля для работы с файловой системой

class MyHTTPServer:
    def __init__(self, host='127.0.0.1', port=8090):
        self.host = host  # Установка хоста, на котором будет работать сервер
        self.port = port  # Установка порта для сервера
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создание сокета
        self.server_socket.bind((self.host, self.port))  # Привязка сокета к адресу и порту
        self.server_socket.listen(5)  # Прослушивание входящих подключений
        print(f"Сервер запущен на {self.host}:{self.port}")

        self.grades = {}  # Инициализация словаря для хранения оценок

    def serve_forever(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()  # Принятие входящего подключения
                self.serve_client(client_socket)  # Обработка полученного клиентского соединения
        except KeyboardInterrupt:
            print("\nОстановка сервера.")  # Обработка остановки сервера
        finally:
            self.server_socket.close()  # Закрытие сокета при завершении работы

    def serve_client(self, client_socket):
        try:
            while True:
                request = client_socket.recv(1024).decode('utf-8')  # Получение и декодирование запроса от клиента
                if not request:
                    return

                method, url, headers, body = self.parse_request(request)  # Разбор HTTP-запроса

                if method == "GET":
                    self.handle_get(client_socket)  # Обработка GET-запроса
                elif method == "POST":
                    self.handle_post(client_socket, body)  # Обработка POST-запроса
                else:
                    self.send_response(client_socket, "405 Method Not Allowed", "Метод не поддерживается.")
                    # Отправка ответа о неподдерживаемом методе
        finally:
            client_socket.close()  # Закрытие клиентского сокета

    def parse_request(self, request):
        lines = request.split("\r\n")  # Разделение запроса на строки
        method, url, protocol = lines[0].split(" ")  # Извлечение метода, URL и протокола из запроса

        headers = {}
        body = ''
        i = 1
        while lines[i]:  # Разбор заголовков HTTP-запроса
            if ": " in lines[i]:
                key, value = lines[i].split(": ", 1)
                headers[key] = value
            i += 1
        if i < len(lines) - 1:  # Извлечение тела запроса, если оно есть
            body = lines[i + 1]

        return method, url, headers, body  # Возврат разобранного метода, URL, заголовков и тела

    def handle_get(self, client_socket):
        if os.path.exists('index.html'):  # Проверка наличия файла index.html
            with open('index.html', 'r', encoding='utf-8') as file:
                response_body = file.read()

            grades_html = '<ul>'  # Создание HTML-списка с оценками
            for discipline, grades in self.grades.items():
                grades_html += f"<li>{discipline}: {', '.join(grades)}</li>"
            grades_html += '</ul>'

            # Замена метки на HTML, содержащий список дисциплин с оценками
            response_body = response_body.replace('<!-- Здесь заполняется список дисциплин с оценками -->', grades_html)
        else:
            # Ответ, если файл index.html не найден
            response_body = "<html><body><h1>Файл index.html не найден</h1></body></html>"

        self.send_response(client_socket, "200 OK", response_body)  # Отправка ответа клиенту

    def handle_post(self, client_socket, body):
        params = {}
        for pair in body.split("&"):  # Разделение тела запроса на параметры. Функция handle_post разделяет это тело запроса именно на такие пары "ключ=значение". Ключи представляют собой имена параметров (discipline и grade в примере), а значения — соответствующие им данные.
            key, value = pair.split("=")
            params[key] = value

        discipline = params.get('discipline', '').replace('+', ' ')  # Извлечение и декодирование параметров
        grade = params.get('grade', '')

        if discipline and grade:  # Если дисциплина и оценка указаны
            if discipline in self.grades:
                self.grades[discipline].append(grade)  # Добавление оценки для существующей дисциплины
            else:
                self.grades[discipline] = [grade]
            self.handle_get(client_socket)
        else:
            self.send_response(client_socket, "400 Bad Request",
                               "<html><body><h1>Неверный запрос!</h1><a href='/'>Назад</a></body></html>")

    def send_response(self, client_socket, status, body):
        response = f"HTTP/1.1 {status}\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        client_socket.sendall(response.encode('utf-8'))


if __name__ == '__main__':
    server = MyHTTPServer(host='127.0.0.1', port=8090)
    server.serve_forever()
