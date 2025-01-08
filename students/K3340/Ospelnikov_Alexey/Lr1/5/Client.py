import os
import http.client
import webbrowser


class HTTPClient:
    def __init__(self):
        self.conn = None

    def connect_to(self, ip, port):
        self.conn = http.client.HTTPConnection(ip, port)

    def post_mark(self, subj, grade):
        if not self.conn:
            raise Exception('No connection provided')
        self.conn.request('POST', f"/grades?subject={subj}&mark={grade}")
        serv_response = self.conn.getresponse()
        print(serv_response.status, serv_response.reason)

    def get_marks(self, subj):
        if not self.conn:
            raise Exception('No connection provided')
        self.conn.request('GET', f"/grades?subject={subj}")
        serv_response = self.conn.getresponse()
        path = "html/client.html"
        body = serv_response.read()
        with open(path, "wb") as cli_html:
            cli_html.write(body)
        webbrowser.open('file://' + os.path.realpath(path), new=2)


if __name__ == "__main__":
    _ip, _port = '127.0.0.1', 8080
    client = HTTPClient()
    while True:
        client.connect_to(_ip, _port)
        subject = input("Выберите предмет: ")
        choice = int(input("1 - Выставить(POST) оценку\n2 - Получить(GET) оценки\n"))
        if choice == 1:
            mark = int(input("Введите оценку от 2(неуд) до 5(отл): "))
            if mark < 2 or mark > 5:
                raise Exception('Оценка должна быть от 2(неуд) до 5(отл)')
            client.post_mark(subject, mark)
            continue
        client.get_marks(subject)