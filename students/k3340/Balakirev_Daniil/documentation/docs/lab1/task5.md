# Задание 5

## Текст задания

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python. Сервер должен: Принять и записать информацию о дисциплине и оценке по дисциплине. Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

## Код

### index.html

    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Журнал</title>
    </head>
    <body>
        <h1>Добавить оценку</h1>
        <form action="/" method="post">
            <label for="subject">Предмет:</label>
            <input type="text" name="subject" id="subject"/>
            <br>
            <label for="grade">Оценка:</label>
            <input type="number" name="grade" id="grade"/>
            <br>
            <button type="submit">Обновить журнал</button>
        </form>
    </body>
    </html>

### server.py

    import socket
    from urllib.parse import parse_qs
    
    class MyHTTPServer:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.journal = {}
    
        def serve_forever(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.host, self.port))
            sock.listen()
            while True:
                client_socket, _ = sock.accept()
                self.serve_client(client_socket)
    
        def serve_client(self, client_socket):
            data = client_socket.recv(4096).decode('utf-8')
            request = self.parse_request(data)
            response = self.handle_request(request)
            if response:
                client_socket.send(response.encode('utf-8'))
                client_socket.close()
    
        def parse_request(self, data):
            data_split = data.split('\r\n')
            print(f"Разделенные данные: {data_split}")
            headers = data_split[0].split()
            print(f"Заголовки: {headers}")
            body = data_split[-1]
            request = dict()
    
            if len(headers) == 3:
                request.update({"method": headers[0], "url": headers[1], "version": headers[2]})
    
                if body:
                    request.update({"parametrs": parse_qs(body)})
                else:
                    request.update({"parametrs": {}})
                return request
            else:
                raise Exception("Неверная строка запроса")
    
        def handle_request(self, request):
            print(request)
            response = f"{request['version']} 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            if request["url"] == "/":
                if request["method"] == "POST":
                    params = request["parametrs"]
                    subject = params.get('subject', [''])[0]
                    grade_str = params.get('grade', [''])[0]
    
                    try:
                        grade = int(grade_str)
                        if subject:
                            if subject in self.journal:
                                self.journal[subject].append(grade)
                            else:
                                self.journal[subject] = [grade]
                    except ValueError:
                        print("Неверный формат оценки")
    
                with open('index.html', encoding='utf-8') as f:
                    response += f.read()
                    return response
    
            if request["url"] == "/grades":
                response += "<html><head><meta charset='UTF-8'><title>Журнал</title></head><body>"
                for subject, grades in self.journal.items():
                    response += f"<h3>{subject}:</h3>"
                    response += "<p>" + ", ".join(map(str, grades)) + "</p>"
                response += "</body></html>"
                return response
    
    if __name__ == "__main__":
        host = 'localhost'
        port = 8000
        myserver = MyHTTPServer(host, port)
        try:
            myserver.serve_forever()
        except KeyboardInterrupt:
            pass
