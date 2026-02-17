import socket

def display_menu():
    """Отображает меню для пользователя"""
    print("\n" + "="*50)
    print("КЛИЕНТ ДЛЯ РАСЧЕТА ПЛОЩАДИ ПАРАЛЛЕЛОГРАММА")
    print("="*50)
    print("Формула: Площадь = основание × высота")
    print("Пример ввода: 5,3 (основание 5, высота 3)")
    print("Команды:")
    print("  - Введите числа через запятую для расчета")
    print("  - 'exit' для выхода")
    print("="*50)

def start_client():
    """Запускает TCP клиент"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = ('localhost', 8082)
    
    print("Клиент запущен")
    
    try:
        client_socket.connect(server_address)
        print(f"Успешно подключен к серверу {server_address}")
        
        display_menu()
        
        while True:
            user_input = input("\nВведите основание и высоту (через запятую): ").strip()
            
            if user_input.lower() == 'exit':
                client_socket.send('exit'.encode('utf-8'))
                print("Завершение работы клиента...")
                break
            
            if not user_input:
                print("Ошибка: Введите данные")
                continue
            
            if ',' not in user_input:
                print("Ошибка: Используйте формат 'основание,высота'")
                continue
            
            client_socket.send(user_input.encode('utf-8'))
            
            response = client_socket.recv(1024).decode('utf-8')
            
            print(f"\nРезультат: {response}")
            
            continue_calc = input("\nПродолжить вычисления? (y/n): ").strip().lower()
            if continue_calc != 'y':
                client_socket.send('exit'.encode('utf-8'))
                print("Завершение работы...")
                break
                
    except ConnectionRefusedError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except KeyboardInterrupt:
        print("\nКлиент остановлен пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        client_socket.close()
        print("Соединение закрыто")

if __name__ == "__main__":
    start_client()