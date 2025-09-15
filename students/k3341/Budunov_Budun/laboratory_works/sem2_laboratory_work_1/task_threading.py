import threading
import time
from parse_functions import worker, parse_and_save

def calculate_sum(start, end, result_dict, index):
    """Вычисляет сумму чисел в диапазоне [start, end]"""
    total = sum(range(start, end + 1))
    result_dict[index] = total

def task_1():
    start_time = time.time()
    
    # Количество потоков
    num_threads = 4
    
    # Разделение диапазона на части
    chunk_size = 1_000_000_000 // num_threads
    
    # Словарь для хранения результатов
    results = {}
    
    # Создание и запуск потоков
    threads = []
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < num_threads - 1 else 1_000_000_000
        thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()
    
    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()
    
    # Суммирование результатов
    total_sum = sum(results.values())
    
    end_time = time.time()
    
    print(f"Сумма чисел от 1 до 1,000,000,000: {total_sum}")
    print(f"Время выполнения (threading): {end_time - start_time:.4f} секунд")

def task_2_threading(tag_name="THREAD_DEFAULT"):
    # Список URL для парсинга (OpenAlex API с разными курсорами)
    base_url = "https://api.openalex.org/works?per-page=50&page="
    urls = [
        f"{base_url}{i+1}" for i in range(20)
    ]
    
    # Количество потоков
    num_threads = 4
    
    # Разделяем URLs на равные части для каждого потока
    chunk_size = len(urls) // num_threads
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    
    # Создаем и запускаем потоки
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(url_chunks[i], tag_name,))
        threads.append(thread)
        thread.start()
    
    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"Threading: Общее время выполнения: {end_time - start_time:.2f} секунд")

def task_2(url: str, tag_name: str = "threading"):
    """
    Парсит один URL в потоке.
    
    Args:
        url (str): URL-адрес для парсинга
        tag_name (str): Имя тега
    
    Returns:
        list: Список заголовков
    """
    start_time = time.time()
    result = parse_and_save(url, tag_name)
    end_time = time.time()
    print(f"Threading: Время выполнения для {url}: {end_time - start_time:.2f} секунд")
    return result

if __name__ == "__main__":
    task_1() # 16.11
    # task_2("task_threading") # 6.67 secs
