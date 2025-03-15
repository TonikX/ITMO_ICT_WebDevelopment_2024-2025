### Задание 5:

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Сервер должен:
- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Ход работы:

#### server.py

```
import socket


def parse_request(data):
    data_split = data.split('\r\n')
    print(f"data split : {data_split}")
    headers = data_split[0].split()
    print(f"Headers : {headers}")
    body = data_split[-1]
    request = dict()

    if len(headers) == 3:

        request.update(
            {"method": headers[0], "url": headers[1], "version": headers[2]})

        if "&" in body:
            parametre = body.split("&")
            request.update({"parametrs": parametre})
            return request
        else:
            request.update({"parametrs": {}})
            return request
    else:
        raise Exception("Malformed request line")


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.grade = []

    def serve_forever(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()
        while True:
            client_socket, _ = sock.accept()
            self.serve_client(client_socket)

    def serve_client(self, client_socket):
        data = client_socket.recv(4096).decode('utf-8')
        request = parse_request(data)
        response = self.handle_request(request)
        if response:
            client_socket.send(response.encode('utf-8'))
            client_socket.close()

    def handle_request(self, request):
        print(request)
        response = f"{request['version']} 200 OK\n\n"
        if request["url"] == "/":
            if request["method"] == "POST":
                self.grade.extend(request["parametrs"])
            if request["method"] == "GET" or "POST":
                with open('index.html', encoding='utf-8') as f:
                    response += f.read()
                    return response
        if request["url"] == "/journal":
            response += "<html><head><title>List grades</title></head><body>"
            for s in self.grade:
                response += f"<p>{s} </p>"
            response += "</body></html>"
            return response


if __name__ == "__main__":
    host = 'localhost'
    port = 8080
    myserver = MyHTTPServer(host, port)
    try:
        myserver.serve_forever()
    except KeyboardInterrupt:
        pass
```

В данном задании объединяем знания работы с html-структурой из 3 задания и внедрения библиотека 
threading из 4 задания.

После успешной настройки сокета и соединения хоста настраиваем прослушивание запросов. Пока 
программа работает, сервер принимает запросы клиентов, сообщая об их активной работе, и 
запускает потоки для работы многих клиентов одновременно. Потоки работают на основе функции 
`client_handler`, обрабатывая запросы. При методе GET сервер формирует таблицу с записанными 
оценками, при методе POST записывает новые пары предмет-оценка в список отметок.

Чтобы убедиться в работе сайта, переходим по заданному адресу `http://localhost:8080`
