# Задание 5: Веб-сервер для управления оценками

## Описание

Реализован веб-сервер для обработки GET и POST HTTP-запросов, позволяющий добавлять оценки по дисциплинам и просматривать их в виде HTML страницы.

## Функциональность

- **GET /** - отображает все оценки в виде HTML таблицы
- **POST /add** - добавляет новую оценку (параметры: subject, grade)
- Данные сохраняются в файл `grades.txt`
- Поддержка среднего балла по дисциплинам

## Файлы реализации

- `server.py` - Веб-сервер
- `Index.html` - Шаблон HTML страницы
- `grades.txt` - Файл для хранения данных

## Код сервера

```python
import socket
import threading
from urllib.parse import parse_qs
from datetime import datetime
import os

class GradesHTTPServer:
    def __init__(self, host='localhost', port=8085):
        self.host = host
        self.port = port
        self.server_socket = None
        self.grades = {} 
        self.lock = threading.Lock()  
        
    def load_grades_from_file(self):
        """Загружает оценки из файла при запуске"""
        try:
            if os.path.exists('grades.txt'):
                with open('grades.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and ':' in line:
                            subject, grade = line.split(':', 1)
                            subject = subject.strip()
                            grade = grade.strip()
                            if subject and grade:
                                if subject not in self.grades:
                                    self.grades[subject] = []
                                self.grades[subject].append(grade)
                print(f"Загружено {len(self.grades)} дисциплин с оценками")  
        except Exception as e:
            print(f"Ошибка при загрузке оценок: {e}")
    
    def save_grades_to_file(self):
        """Сохраняет оценки в файл"""
        try:
            with open('grades.txt', 'w', encoding='utf-8') as f:
                for subject, grades_list in self.grades.items():
                    for grade in grades_list:
                        f.write(f"{subject}:{grade}\n")
        except Exception as e:
            print(f"Ошибка при сохранении оценок: {e}")
    
    def add_grade(self, subject, grade):
        """Добавляет оценку по дисциплине"""
        with self.lock:
            if subject not in self.grades:
                self.grades[subject] = []
            self.grades[subject].append(grade)
            self.save_grades_to_file()
    
    def generate_html_page(self):
        """Генерирует HTML-страницу со всеми оценками"""
        try:
            with open('Index.html', 'r', encoding='utf-8') as f:
                template = f.read()
        except FileNotFoundError:
            return '<html><body><h1>Ошибка: файл Index.html не найден</h1></body></html>'
        
        grades_html = ''
        if not self.grades:
            grades_html = '<div class="empty">Пока нет оценок. Добавьте первую оценку!</div>'
        else:
            for subject, grades in sorted(self.grades.items()):
                grades_html += f'''
                <div class="subject">
                    <h3>{subject}</h3>
                    <div class="grades">
                '''
                
                for grade in grades:
                    grades_html += f'<span class="grade">{grade}</span>'
                
                numeric_grades = []
                for grade in grades:
                    if grade.isdigit():
                        numeric_grades.append(int(grade))
                
                if numeric_grades:
                    average = sum(numeric_grades) / len(numeric_grades)
                    grades_html += f'<div class="avg">Средний балл: {average:.2f}</div>'
                
                grades_html += f'''
                    </div>
                    <small>Всего оценок: {len(grades)}</small>
                </div>
                '''
        
        footer_html = f'''
        <div>Сервер запущен: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</div>
        <div>Всего дисциплин: {len(self.grades)}</div>
        '''
        
        html = template.replace('{{GRADES}}', grades_html).replace('{{FOOTER}}', footer_html)
        
        return html
    
    def handle_request(self, client_socket, client_address):
        """Обрабатывает HTTP-запрос"""
        try:
            request_data = client_socket.recv(4096).decode('utf-8')
            
            if not request_data:
                return
            
            lines = request_data.split('\n')
            request_line = lines[0].strip()
            parts = request_line.split()
            
            if len(parts) < 3:
                self.send_response(client_socket, 400, 'Bad Request')
                return
            
            method = parts[0]
            path = parts[1]
            
            # Разбираем заголовки
            headers = {}
            body_start = request_data.find('\r\n\r\n')
            if body_start != -1:
                body = request_data[body_start + 4:]
            else:
                body = ''
            
            print(f"{method} {path} from {client_address}")
            
            if method == 'GET' and path == '/':
                html_content = self.generate_html_page()
                self.send_response(client_socket, 200, 'text/html', html_content)
                
            elif method == 'POST' and path == '/add':
                if body:
                    try:
                        params = parse_qs(body)
                        subject = params.get('subject', [''])[0].strip()
                        grade = params.get('grade', [''])[0].strip()
                        
                        if subject and grade:
                            self.add_grade(subject, grade)
                            # Перенаправляем на главную страницу
                            response = '''HTTP/1.1 302 Found\r\nLocation: /\r\nContent-Length: 0\r\n\r\n'''
                            client_socket.send(response.encode('utf-8'))
                        else:
                            self.send_response(client_socket, 400, 'text/plain', 'Missing subject or grade')
                    except Exception as e:
                        self.send_response(client_socket, 400, 'text/plain', f'Error parsing request: {str(e)}')
                else:
                    self.send_response(client_socket, 400, 'text/plain', 'No body in POST request')
            else:
                self.send_response(client_socket, 404, 'text/plain', 'Not Found')
                
        except Exception as e:
            print(f"Error handling request: {e}")
            try:
                self.send_response(client_socket, 500, 'text/plain', 'Internal Server Error')
            except:
                pass
        finally:
            client_socket.close()
    
    def send_response(self, client_socket, status_code, content_type, content):
        """Отправляет HTTP ответ"""
        status_messages = {
            200: 'OK',
            302: 'Found',
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
        
        response = f'''HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n'''
        response += f'Content-Type: {content_type}; charset=utf-8\r\n'
        response += f'Content-Length: {len(content)}\r\n'
        response += f'Server: GradesServer/1.0\r\n'
        response += f'Date: {datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}\r\n'
        response += '\r\n'
        response += content
        
        client_socket.send(response.encode('utf-8'))
    
    def start(self):
        """Запускает сервер"""
        self.load_grades_from_file()
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"Сервер оценок запущен на http://{self.host}:{self.port}")
        print("Доступные endpoints:")
        print("  GET  /     - просмотр всех оценок")
        print("  POST /add  - добавление оценки (subject, grade)")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Подключение от {client_address}")
                
                client_thread = threading.Thread(
                    target=self.handle_request,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nОстановка сервера...")
        finally:
            self.save_grades_to_file()
            self.server_socket.close()

if __name__ == "__main__":
    server = GradesHTTPServer()
    server.start()
```

## HTML шаблон

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Журнал оценок</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }

        .add-form {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #007bff;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #007bff;
        }

        button {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background: #0056b3;
        }

        .subjects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .subject {
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .subject:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .subject h3 {
            color: #007bff;
            margin-top: 0;
            margin-bottom: 15px;
            border-bottom: 2px solid #007bff;
            padding-bottom: 5px;
        }

        .grades {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 10px;
        }

        .grade {
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }

        .grade:nth-child(2n) {
            background: #17a2b8;
        }

        .grade:nth-child(3n) {
            background: #ffc107;
            color: #212529;
        }

        .avg {
            background: #6c757d;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 10px;
            display: inline-block;
        }

        .empty {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
            background: #f8f9fa;
            border-radius: 8px;
            grid-column: 1 / -1;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #6c757d;
            font-size: 14px;
        }

        small {
            color: #6c757d;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Журнал оценок</h1>
        
        <div class="add-form">
            <h2>➕ Добавить оценку</h2>
            <form method="POST" action="/add">
                <div class="form-group">
                    <label for="subject">Дисциплина:</label>
                    <input type="text" id="subject" name="subject" required placeholder="Например: Математика">
                </div>
                <div class="form-group">
                    <label for="grade">Оценка:</label>
                    <input type="text" id="grade" name="grade" required placeholder="Например: 5 (отлично)">
                </div>
                <button type="submit">Добавить оценку</button>
            </form>
        </div>

        <div class="subjects-grid">
            {{GRADES}}
        </div>

        <div class="footer">
            {{FOOTER}}
        </div>
    </div>
</body>
</html>
```

## Запуск

1. Запустите сервер: `python server.py`
2. Откройте браузер и перейдите на http://localhost:8085
3. Добавляйте оценки через форму и просматривайте статистику