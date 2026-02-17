import socket
import math

def calculate_parallelogram_area(base, height):
    """Вычисляет площадь параллелограмма: S = base * height"""
    return base * height

def handle_client_connection(client_socket, client_address):
    """Обрабатывает соединение с клиентом"""
    print(f"Подключен клиент: {client_address}")
    
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            
            if not data:
                print(f"Клиент {client_address} отключился")
                break
            
            if data.lower() == 'exit':
                print(f"Клиент {client_address} запросил отключение")
                client_socket.send("Сервер завершил соединение".encode('utf-8'))
                break
            
            print(f"Получены данные от клиента: {data}")
            
            try:
                base, height = map(float, data.split(','))
                
                area = calculate_parallelogram_area(base, height)
                
                response = f"Площадь параллелограмма с основанием {base} и высотой {height} = {area:.2f}"
                
            except ValueError as e:
                response = f"Ошибка: Неверный формат данных. Ожидается: основание,высота. Пример: 5,3"
            except Exception as e:
                response = f"Ошибка при вычислении: {str(e)}"
            
            client_socket.send(response.encode('utf-8'))
            print(f"Отправлен ответ: {response}")
            
    except ConnectionResetError:
        print(f"Клиент {client_address} неожиданно отключился")
    except Exception as e:
        print(f"Ошибка при работе с клиентом {client_address}: {str(e)}")
    finally:
        client_socket.close()
        print(f"Соединение с клиентом {client_address} закрыто")

def start_server():
    """Запускает TCP сервер"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = ('localhost', 8082)  
    server_socket.bind(server_address)
    server_socket.listen(5)
    
    print("TCP Сервер запущен и слушает на localhost:12346")
    print("Ожидание подключений...")
    print("Для остановки сервера нажмите Ctrl+C")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            
            handle_client_connection(client_socket, client_address)
            
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        server_socket.close()
        print("Серверный сокет закрыт")

if __name__ == "__main__":
    start_server()