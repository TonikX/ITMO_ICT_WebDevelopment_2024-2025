import socket
import threading
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=8084):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {} 
        self.running = True
        self.lock = threading.Lock()  
        
    def broadcast_message(self, message, sender_socket=None):
        """Отправляет сообщение всем подключенным клиентам, кроме отправителя"""
        with self.lock:
            disconnected_clients = []
            
            for client_socket, client_info in self.clients.items():
                try:
                    if client_socket != sender_socket:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        formatted_message = f"[{timestamp}] {message}\n"
                        client_socket.send(formatted_message.encode('utf-8'))
                except (BrokenPipeError, ConnectionResetError, OSError):
                    disconnected_clients.append(client_socket)
            
            for client_socket in disconnected_clients:
                if client_socket in self.clients:
                    username = self.clients[client_socket]['username']
                    print(f"Клиент {username} отключился (ошибка отправки)")
                    del self.clients[client_socket]
                    client_socket.close()
    
    def handle_client(self, client_socket, client_address):
        """Обрабатывает соединение с одним клиентом"""
        username = None
        
        try:
            client_socket.send("Введите ваше имя: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
            
            if not username:
                username = f"Гость_{client_address[1]}"
            
            with self.lock:
                self.clients[client_socket] = {
                    'username': username,
                    'address': client_address,
                    'join_time': datetime.now()
                }
            
            join_message = f">>> {username} присоединился к чату!"
            print(join_message)
            self.broadcast_message(join_message, client_socket)
            
            welcome_msg = f"\nДобро пожаловать в чат, {username}!\n" \
                         f"Сейчас в чате: {len(self.clients)} пользователь(ей)\n" \
                         f"Команды:\n" \
                         f"/online - список онлайн пользователей\n" \
                         f"/quit - выход из чата\n" \
                         "="*50 + "\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8').strip()
                    
                    if not message:
                        break  
                    
                    if message.startswith('/'):
                        if message == '/quit':
                            break
                        else:
                            client_socket.send("Неизвестная команда. Используйте /help для списка команд.".encode('utf-8'))
                    else:
                        chat_message = f"{username}: {message}"
                        print(f"{datetime.now().strftime('%H:%M:%S')} {chat_message}")
                        self.broadcast_message(chat_message, client_socket)
                        
                except (ConnectionResetError, BrokenPipeError):
                    break
                except UnicodeDecodeError:
                    client_socket.send("Ошибка: неверная кодировка сообщения".encode('utf-8'))
                    
        except Exception as e:
            print(f"Ошибка при работе с клиентом {client_address}: {str(e)}")
        finally:
            if client_socket in self.clients:
                with self.lock:
                    if client_socket in self.clients:
                        username = self.clients[client_socket]['username']
                        del self.clients[client_socket]
                
                if username:
                    leave_message = f"<<< {username} покинул чат."
                    print(leave_message)
                    self.broadcast_message(leave_message)
            
            client_socket.close()
            print(f"Соединение с {client_address} закрыто")
    
    def start_server(self):
        """Запускает сервер"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"Сервер чата запущен на {self.host}:{self.port}")
            print("Для остановки сервера нажмите Ctrl+C")
            print("=" * 50)
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Новое подключение от {client_address}")
                    
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except OSError:
                    break
                    
        except Exception as e:
            print(f"Ошибка при запуске сервера: {str(e)}")
        finally:
            self.stop_server()
    
    def stop_server(self):
        """Останавливает сервер"""
        self.running = False
        
        with self.lock:
            for client_socket in self.clients.keys():
                try:
                    client_socket.send("Сервер остановлен. Соединение разорвано.".encode('utf-8'))
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
        
        if self.server_socket:
            self.server_socket.close()
        
        print("Сервер чата остановлен")
    
    def get_server_info(self):
        """Возвращает информацию о сервере"""
        with self.lock:
            return {
                'host': self.host,
                'port': self.port,
                'clients_count': len(self.clients),
                'clients': [info['username'] for info in self.clients.values()]
            }

def main():
    """Основная функция запуска сервера"""
    server = ChatServer('localhost', 8888)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        server.stop_server()

if __name__ == "__main__":
    main()