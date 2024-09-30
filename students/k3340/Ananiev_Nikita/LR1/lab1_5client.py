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
        path = "templates/lab1_5client.html"
        body = serv_response.read()
        with open(path, "wb") as cli_html:
            cli_html.write(body)
        webbrowser.open('file://' + os.path.realpath(path), new=2)


if __name__ == "__main__":
    _ip, _port = '127.0.0.1', 7878
    client = HTTPClient()
    while True:
        client.connect_to(_ip, _port)
        subject = input("Choose subject:")
        choice = int(input("Choose POST mark(1) or GET marks(2):"))
        if choice == 1:
            mark = int(input("input mark(1-5):"))
            client.post_mark(subject, mark)
            continue
        client.get_marks(subject)
