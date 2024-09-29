from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import threading

HOST = '127.0.0.1'
PORT = 5555

grade_records = []

class GradeHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html_content = self.build_html_page()
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urlparse.parse_qs(post_data)

        subject = params.get('discipline', [''])[0]
        mark = params.get('grade', [''])[0]

        if subject and mark:
            self.update_grades(subject, mark)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    def update_grades(self, subject, mark):
        existing_entry = next((item for item in grade_records if item['discipline'] == subject), None)
        if existing_entry:
            existing_entry['grade'] += f", {mark}"
        else:
            grade_records.append({'discipline': subject, 'grade': mark})

    def build_html_page(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Оценки</title>
</head>
<body>
    <h1>Список оценок</h1>
    <table border="1">
        <tr><th>Дисциплина</th><th>Оценки</th></tr>"""

        for record in grade_records:
            html += f"<tr><td>{record['discipline']}</td><td>{record['grade']}</td></tr>"

        html += """
    </table>
    <h2>Добавить оценку</h2>
    <form method="POST" action="/">
        <label for="discipline">Дисциплина:</label><br>
        <input type="text" id="discipline" name="discipline" required><br>
        <label for="grade">Оценка:</label><br>
        <input type="text" id="grade" name="grade" required><br><br>
        <input type="submit" value="Добавить">
    </form>
</body>
</html>"""
        return html

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, GradeHTTPRequestHandler)
    print(f"Сервер запущен по адресу http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
