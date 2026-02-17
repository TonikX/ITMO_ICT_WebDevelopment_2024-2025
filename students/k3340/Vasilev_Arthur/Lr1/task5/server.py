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
            request_data = client_socket.recv(1024).decode('utf-8')
            
            if not request_data:
                return
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Запрос от {client_address}")
            
            lines = request_data.split('\n')
            if not lines:
                return
            
            first_line = lines[0]
            parts = first_line.split()
            
            if len(parts) < 2:
                self.send_error(client_socket, 400, "Bad Request")
                return
            
            method = parts[0]
            path = parts[1]
            
            print(f"Метод: {method}, Путь: {path}")
            
            if method == 'GET':
                self.handle_get(client_socket, path)
            elif method == 'POST':
                content_length = 0
                for line in lines:
                    if line.startswith('Content-Length:'):
                        content_length = int(line.split(':')[1].strip())
                        break
                
                body = ''
                if content_length > 0:
                    if '\r\n\r\n' in request_data:
                        body = request_data.split('\r\n\r\n', 1)[1]
                    if len(body) < content_length:
                        remaining = content_length - len(body)
                        body += client_socket.recv(remaining).decode('utf-8')
                
                self.handle_post(client_socket, path, body)
            else:
                self.send_error(client_socket, 405, "Method Not Allowed")
                
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            self.send_error(client_socket, 500, "Internal Server Error")
        finally:
            client_socket.close()
    
    def handle_get(self, client_socket, path):
        """Обрабатывает GET запрос"""
        if path == '/' or path == '/index.html':
            html_content = self.generate_html_page()
            response = self.create_response(200, 'text/html; charset=utf-8', html_content)
        else:
            error_html = '''
            <!DOCTYPE html>
            <html>
            <head><title>404 Not Found</title></head>
            <body>
                <h1>404 - Страница не найдена</h1>
                <p><a href="/">Вернуться на главную</a></p>
            </body>
            </html>
            ''' 
            response = self.create_response(404, 'text/html; charset=utf-8', error_html)
        
        client_socket.send(response)
    
    def handle_post(self, client_socket, path, body):
        """Обрабатывает POST запрос"""
        if path == '/':
            try:
                parsed_data = parse_qs(body)
                
                subject = parsed_data.get('subject', [''])[0].strip()
                grade = parsed_data.get('grade', [''])[0].strip()
                
                if subject and grade:
                    self.add_grade(subject, grade)
                    print(f"Добавлена оценка: {subject} - {grade}")
                    
                    redirect_html = f'''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Оценка добавлена</title>
                        <meta http-equiv="refresh" content="1;url=/" />
                    </head>
                    <body>
                        <h1>Оценка успешно добавлена!</h1>
                        <p>Перенаправление на главную страницу...</p>
                        <p><a href="/">Вернуться сразу</a></p>
                    </body>
                    </html>
                    '''  
                    response = self.create_response(200, 'text/html; charset=utf-8', redirect_html)
                else:
                    error_html = '''
                    <!DOCTYPE html>
                    <html>
                    <head><title>Ошибка</title></head>
                    <body>
                        <h1>Ошибка: заполните все поля</h1>
                        <p><a href="/">Вернуться назад</a></p>
                    </body>
                    </html>
                    '''  
                    response = self.create_response(400, 'text/html; charset=utf-8', error_html)
                    
            except Exception as e:
                print(f"Ошибка при обработке POST: {e}")
                response = self.create_response(500, 'text/html; charset=utf-8', 'Internal Server Error')
        else:
            response = self.create_response(404, 'text/html; charset=utf-8', 'Not Found')
        
        client_socket.send(response)
    
    def create_response(self, status_code, content_type, content):
        """Создает HTTP-ответ"""
        status_messages = {
            200: 'OK',
            400: 'Bad Request',
            404: 'Not Found',
            405: 'Method Not Allowed',
            500: 'Internal Server Error'
        }
        
        response_headers = [
            f'HTTP/1.1 {status_code} {status_messages.get(status_code, "Unknown")}',
            f'Content-Type: {content_type}',
            f'Content-Length: {len(content)}',
            'Server: GradesHTTPServer/1.0',
            'Connection: close',
            ''
        ]
        
        return '\r\n'.join(response_headers).encode('utf-8') + content.encode('utf-8')
    
    def send_error(self, client_socket, status_code, message):
        """Отправляет ошибку"""
        response = self.create_response(status_code, 'text/plain', message)
        client_socket.send(response)
    
    def start_server(self):
        """Запускает сервер"""
        self.load_grades_from_file()
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"Сервер оценок запущен на http://{self.host}:{self.port}")  
            print("Функциональность:")
            print("   - GET / - просмотр всех оценок")  
            print("   - POST / - добавление новой оценки") 
            print("   - Данные сохраняются в файл grades.txt") 
            print("Для остановки нажмите Ctrl+C") 
            print("=" * 50)
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                
                client_thread = threading.Thread(
                    target=self.handle_request,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nОстановка сервера...") 
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
            print("Сервер остановлен") 

def main():
    """Основная функция"""
    server = GradesHTTPServer('localhost', 8080)
    server.start_server()

if __name__ == "__main__":
    main()