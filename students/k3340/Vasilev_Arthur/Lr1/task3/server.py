import socket
import os
import datetime

class SimpleHTTPServer:
    def __init__(self, host='localhost', port=8083):
        self.host = host
        self.port = port
        self.server_socket = None
        
    def create_http_response(self, status_code, content_type, content):
        """Создает HTTP-ответ с заданными параметрами"""
        # Статусная строка
        status_messages = {
            200: 'OK',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
        
        response_headers = [
            f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(content)}",
            f"Server: SimplePythonHTTPServer/1.0",
            f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
            "Connection: close",
            ""  
        ]
        
        response = "\r\n".join(response_headers) + content
        return response.encode('utf-8')
    
    def handle_request(self, client_socket):
        """Обрабатывает HTTP-запрос от клиента"""
        try:
            request_data = client_socket.recv(1024).decode('utf-8')
            print("=" * 50)
            print(f"Получен запрос:\n{request_data}")
            
            if not request_data:
                return
            
            first_line = request_data.split('\n')[0]
            parts = first_line.split()
            
            if len(parts) < 2:
                response = self.create_http_response(400, 'text/plain', 'Bad Request')
                client_socket.send(response)
                return
            
            method = parts[0]
            path = parts[1]
            
            print(f"Метод: {method}, Путь: {path}")
            
            if method != 'GET':
                response = self.create_http_response(405, 'text/plain', 'Method Not Allowed')
                client_socket.send(response)
                return
            
            if path == '/':
                path = '/index.html'
            
            file_path = path[1:] if path.startswith('/') else path
            
            if '..' in file_path or file_path.startswith('/'):
                response = self.create_http_response(403, 'text/plain', 'Forbidden')
                client_socket.send(response)
                return
            
            if not file_path:
                file_path = 'index.html'
            
            print(f"Пытаемся открыть файл: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                content_types = {
                    '.html': 'text/html; charset=utf-8',
                    '.css': 'text/css',
                    '.js': 'application/javascript',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.json': 'application/json',
                    '.txt': 'text/plain'
                }
                
                _, ext = os.path.splitext(file_path)
                content_type = content_types.get(ext.lower(), 'text/plain')
                
                response = self.create_http_response(200, content_type, content)
                print(f"Файл {file_path} успешно отправлен")
                
            except FileNotFoundError:
                error_html = """
                <!DOCTYPE html>
                <html>
                <head><title>404 Not Found</title></head>
                <body>
                    <h1>404 - Страница не найдена</h1>
                    <p>Запрашиваемый файл не существует на сервере.</p>
                    <p><a href="/">Вернуться на главную</a></p>
                </body>
                </html>
                """
                response = self.create_http_response(404, 'text/html', error_html)
                print(f"Файл {file_path} не найден")
                
            except Exception as e:
                error_html = f"""
                <!DOCTYPE html>
                <html>
                <head><title>500 Server Error</title></head>
                <body>
                    <h1>500 - Внутренняя ошибка сервера</h1>
                    <p>Произошла ошибка: {str(e)}</p>
                </body>
                </html>
                """
                response = self.create_http_response(500, 'text/html', error_html)
                print(f"Ошибка при чтении файла: {str(e)}")
            
            client_socket.send(response)
            
        except Exception as e:
            print(f"Ошибка при обработке запроса: {str(e)}")
            try:
                error_response = self.create_http_response(500, 'text/plain', 'Internal Server Error')
                client_socket.send(error_response)
            except:
                pass
    
    def start(self):
        """Запускает HTTP-сервер"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.server_socket.bind((self.host, self.port))
        
        self.server_socket.listen(5)
        
        print(f"HTTP-сервер запущен на http://{self.host}:{self.port}")
        print(f"Рабочая директория: {os.getcwd()}")
        print("Для остановки сервера нажмите Ctrl+C")
        print("=" * 50)
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Новое подключение от {client_address}")
                
                self.handle_request(client_socket)
                
                client_socket.close()
                print(f"Соединение с {client_address} закрыто")
                
        except KeyboardInterrupt:
            print("\nСервер остановлен пользователем")
        finally:
            if self.server_socket:
                self.server_socket.close()
            print("Серверный сокет закрыт")

def main():
    """Основная функция"""
    server = SimpleHTTPServer('localhost', 8080)
    server.start()

if __name__ == "__main__":
    main()