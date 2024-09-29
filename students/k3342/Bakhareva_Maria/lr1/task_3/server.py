import socket
import os

# Путь к HTML-файлу
HTML_FILE = 'index.html'


def load_html_file():
    """Загружает содержимое HTML-файла."""
    if not os.path.exists(HTML_FILE):
        return "HTTP/1.1 404 Not Found\n\n404 Not Found"

    with open(HTML_FILE, 'r') as file:
        return file.read()


def start_server():
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    print("Сервер запущен и ожидает подключения на порту 8080...")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Подключено к {addr}")

            try:
                request = conn.recv(1024).decode()
                print(f"Запрос:\n{request}")

                # Загружаем HTML-страницу
                html_content = load_html_file()
                response = "HTTP/1.1 200 OK\n"
                response += "Content-Type: text/html; charset=utf-8\n"
                response += "Connection: close\n\n"
                response += html_content

                # Отправляем ответ
                conn.sendall(response.encode())
            except Exception as e:
                print(f"Ошибка: {e}")
            finally:
                conn.close()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server_socket.close()


# Запускаем сервер
start_server()
