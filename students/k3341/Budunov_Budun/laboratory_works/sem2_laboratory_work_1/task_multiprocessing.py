import multiprocessing
import time
from parse_functions import worker, parse_and_save

def calculate_sum(start, end):
    """Вычисляет сумму чисел в диапазоне [start, end]"""
    return sum(range(start, end + 1))

def task_1():
    start_time = time.time()
    
    # Количество процессов
    num_processes = multiprocessing.cpu_count()
    
    # Разделение диапазона на части
    chunk_size = 1_000_000_000 // num_processes
    
    # Создание аргументов для процессов
    args = []
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < num_processes - 1 else 1_000_000_000
        args.append((start, end))
    
    # Создание пула процессов и выполнение задач
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(calculate_sum, args)
    
    # Суммирование результатов
    total_sum = sum(results)
    
    end_time = time.time()
    
    print(f"Сумма чисел от 1 до 1,000,000,000: {total_sum}")
    print(f"Время выполнения (multiprocessing): {end_time - start_time:.4f} секунд")

def task_2_multiprocessing(tag_name="MLTPRCSS_DEFAULT"):
    # Список URL для парсинга (OpenAlex API с разными курсорами)
    base_url = "https://api.openalex.org/works?per-page=50&page="
    urls = [
        f"{base_url}{i+1}" for i in range(20)
    ]
    
    # Количество процессов
    num_processes = 4
    
    # Разделяем URLs на равные части для каждого процесса
    chunk_size = len(urls) // num_processes
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    
    # Создаем и запускаем процессы
    processes = []
    start_time = time.time()
    
    for i in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(url_chunks[i], tag_name,))
        processes.append(process)
        process.start()
    
    # Ожидаем завершения всех процессов
    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"Multiprocessing: Общее время выполнения: {end_time - start_time:.2f} секунд")

def task_2(url: str, tag_name: str = "multiprocessing"):
    """
    Парсит один URL.
    
    Args:
        url (str): URL-адрес для парсинга
        tag_name (str): Имя тега
    
    Returns:
        list: Список заголовков
    """
    start_time = time.time()
    result = parse_and_save(url, tag_name)
    end_time = time.time()
    print(f"Multiprocessing: Время выполнения для {url}: {end_time - start_time:.2f} секунд")
    return result

if __name__ == "__main__":
    task_1() # 2.97 secs
    # task_2("task_multiprocessing") # 7.63 secs