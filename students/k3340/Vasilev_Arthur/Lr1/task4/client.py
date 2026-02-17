import socket
import threading
import sys
import time

class ChatClient:
    def __init__(self, host='localhost', port=8084):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = True
        self.username = None
    
    def receive_messages(self):
        """Поток для получения сообщений от сервера"""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    print("\nСоединение с сервером разорвано.")
                    self.running = False
                    break
                
                print(f"\r{message}", end='')
                print("\nВведите сообщение: ", end='', flush=True)
                
            except (ConnectionResetError, BrokenPipeError):
                print("\nПотеряно соединение с сервером")
                self.running = False
                break
            except OSError:
                break
            except Exception as e:
                print(f"\nОшибка при получении сообщения: {str(e)}")
                break
    
    def send_message(self, message):
        """Отправляет сообщение на сервер"""
        try:
            self.client_socket.send(message.encode('utf-8'))
            return True
        except (BrokenPipeError, ConnectionResetError):
            print("Не удалось отправить сообщение: соединение разорвано")
            return False
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {str(e)}")
            return False
    
    def connect(self):
        """Подключается к серверу"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Успешно подключен к серверу {self.host}:{self.port}")
            return True
        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
            return False
        except Exception as e:
            print(f"Ошибка подключения: {str(e)}")
            return False
    
    def start(self):
        """Запускает клиент"""
        if not self.connect():
            return
        
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        print("\n" + "="*50)
        print("Добро пожаловать в многопользовательский чат!")
        print("="*50)
        
        try:
            while self.running:
                try:
                    message = input("Введите сообщение: ").strip()
                except KeyboardInterrupt:
                    print("\nВыход из чата...")
                    break
                except EOFError:
                    break
                
                if not message:
                    continue
                
                if message.lower() in ['/quit', '/exit', 'выход']:
                    print("Выход из чата...")
                    self.send_message('/quit')
                    break
                
                if not self.send_message(message):
                    break
                    
        except KeyboardInterrupt:
            print("\nВыход из чата...")
        finally:
            self.disconnect()
    
    def disconnect(self):
        """Отключается от сервера"""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        print("Соединение закрыто")

def main():
    """Основная функция запуска клиента"""
    host = 'localhost'
    port = 8888
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Ошибка: порт должен быть числом")
            return
    
    client = ChatClient(host, port)
    
    try:
        client.start()
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")

if __name__ == "__main__":
    main()