import socket

# Настройки сервера
HOST = '127.0.0.1'  # Локальный хост
PORT = 8080         # Порт для прослушивания

def load_html_file(file_path):
    """Загружает содержимое HTML-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h1>404 Not Found</h1>"

def start_server():
    """Запускает HTTP-сервер."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Сервер запущен на {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Подключен клиент: {client_address}")

                # Получаем запрос от клиента
                request = client_socket.recv(1024).decode('utf-8')
                print(f"Запрос от клиента:\n{request}")

                # Загружаем HTML-страницу
                response_body = load_html_file(r'C:\code\ITMO_ICT_WebDevelopment_2024-2025\students\k3341\laboratory_works\Konoplia_Aleksei\labaratory_work_1\task3\index.html')

                # Формируем HTTP-ответ
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
                    "\r\n"
                    f"{response_body}"
                )

                # Отправляем ответ клиенту
                client_socket.sendall(response.encode('utf-8'))
                print("Ответ отправлен клиенту")

if __name__ == "__main__":
    start_server()
