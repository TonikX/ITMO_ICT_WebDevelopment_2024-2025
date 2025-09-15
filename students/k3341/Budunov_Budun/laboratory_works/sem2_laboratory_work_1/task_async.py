import asyncio
import time
import functools
from concurrent.futures import ThreadPoolExecutor
from parse_functions import parse_and_save

def calculate_sum(start, end):
    """Вычисляет сумму чисел в диапазоне [start, end]"""
    return sum(range(start, end + 1))

async def run_calculate_sum(start, end):
    """Запускает синхронную функцию calculate_sum в отдельном потоке"""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, calculate_sum, start, end)

async def task_1():
    start_time = time.time()
    
    # Количество задач
    num_tasks = 4
    
    # Разделение диапазона на части
    chunk_size = 1_000_000_000 // num_tasks
    
    # Создание задач
    tasks = []
    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < num_tasks - 1 else 1_000_000_000
        tasks.append(run_calculate_sum(start, end))  # Используем асинхронную обертку
    
    # Запуск задач и ожидание результатов
    results = await asyncio.gather(*tasks)
    
    # Суммирование результатов
    total_sum = sum(results)
    
    end_time = time.time()
    
    print(f"Сумма чисел от 1 до 1,000,000,000: {total_sum}")
    print(f"Время выполнения (async): {end_time - start_time:.4f} секунд")

async def run_in_executor(url, tag_name):
    """
    Запускает синхронную функцию parse_and_save в отдельном потоке.
    
    Args:
        url (str): URL-адрес для парсинга
        tag_name (str): Имя тега
    
    Returns:
        list: Список заголовков
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, 
            functools.partial(parse_and_save, url, tag_name)
        )
        return result

async def task_2(url: str, tag_name: str = "async"):
    """
    Асинхронно парсит один URL.
    
    Args:
        url (str): URL-адрес для парсинга
        tag_name (str): Имя тега для добавления
    
    Returns:
        list: Список заголовков
    """
    start_time = time.time()
    result = await run_in_executor(url, tag_name)
    end_time = time.time()
    print(f"Async: Время выполнения для {url}: {end_time - start_time:.2f} секунд")
    return result

if __name__ == "__main__":
    # asyncio.run(task_1()) # 15.54 secs
    asyncio.run(task_2("task_asnc")) # 3.7 секунд
