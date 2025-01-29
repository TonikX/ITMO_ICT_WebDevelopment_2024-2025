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
