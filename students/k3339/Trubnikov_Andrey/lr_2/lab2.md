# Сравнение методов вычисления суммы чисел

В этом проекте рассматриваются три подхода к вычислению суммы чисел от 1 до 100_000_000:

1. **Асинхронный подход (`asyncio`)**
2. **Многопроцессный подход (`multiprocessing`)**
3. **Многопоточный подход (`threading`)**

---

## 1. Асинхронный подход

```python
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

N = 10 ** 9
NUM_TASKS = 4


def blocking_sum(start, end):
    return sum(range(start, end + 1))


async def calculate_sum():
    step = N // NUM_TASKS
    loop = asyncio.get_running_loop()
    tasks = []

    with ProcessPoolExecutor(max_workers=NUM_TASKS) as executor:
        for i in range(NUM_TASKS):
            start = i * step + 1
            end = (i + 1) * step if i < NUM_TASKS - 1 else N
            tasks.append(loop.run_in_executor(executor, blocking_sum, start, end))

        results = await asyncio.gather(*tasks)

    return sum(results)


async def main():
    start_time = time.time()
    total = await calculate_sum()
    print(f"Asyncio {total}")
    print(f"Execution time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
```

Особенности:

Использует asyncio и корутины.

Эффективно при работе с I/O, но не даёт прироста на CPU-bound задачах.

Примерное время выполнения: ~6.63 с.


# 2. Многопроцессный подход
```python
import multiprocessing
import time

N = 10**9
NUM_PROCESSES = 4

def calculate_sum(start, end):
    return sum(range(start, end + 1))

def main():
    step = N // NUM_PROCESSES
    ranges = [(i * step + 1, (i + 1) * step if i < NUM_PROCESSES - 1 else N)
              for i in range(NUM_PROCESSES)]

    start_time = time.time()
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        results = pool.starmap(calculate_sum, ranges)

    total = sum(results)
    print(f"Multiprocessing result: {total}")
    print(f"Execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()


```


Особенности:

Создаёт отдельные процессы для каждой части задачи.

Хорошо масштабируется на CPU-bound задачах.

Примерное время выполнения: ~5.89 с.



# 3. Многопоточный подход

```python
import threading
import time

N = 10**9
NUM_THREADS = 4
results = [0] * NUM_THREADS

def calculate_sum(start, end, index):
    results[index] = sum(range(start, end + 1))

def main():
    step = N // NUM_THREADS
    threads = []
    start_time = time.time()

    for i in range(NUM_THREADS):
        start = i * step + 1
        end = (i + 1) * step if i < NUM_THREADS - 1 else N
        t = threading.Thread(target=calculate_sum, args=(start, end, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total = sum(results)
    print(f"Threading result: {total}")
    print(f"Execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()


```

Особенности:

Использует потоки в одном процессе.

Подходит для I/O-bound задач.

На CPU-bound задачах выигрыша нет из-за GIL.

Примерное время выполнения: ~21.58 с

# Выводы
Для CPU-bound задач эффективнее использовать multiprocessing.

Для I/O-bound задач подойдут asyncio или threading.

Все методы дают одинаковый результат: 5000000050000000


# Написание парсера

## asyncio

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from math import ceil

from app.dependencies import get_db
from app.crud import crud_category
from app.schemas.category import CategoryCreate

app = FastAPI(title="Asyncio Parser API")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

class ParseRequest(BaseModel):
    urls: List[str]

async def fetch_title(session, url: str):
    try:
        async with session.get(url, timeout=10) as r:
            text = await r.text()
            soup = BeautifulSoup(text, "html.parser")
            t = soup.find("title")
            return t.get_text(strip=True) if t else None
    except Exception as e:
        print(f"[ASYNC] Error fetching {url}: {e}")
        return None

@app.post("/parse")
async def parse(request: ParseRequest):
    db = next(get_db())
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:

        async def worker(url):
            title = await fetch_title(session, url)
            if title:
                cat_data = CategoryCreate(name=title)
                category = crud_category.upsert_category(db, cat_data)
                results.append(category.name)

        try:
            NUM_CHUNKS = 3
            k = ceil(len(request.urls) / NUM_CHUNKS)
            chunks = [request.urls[i * k:(i + 1) * k] for i in range(NUM_CHUNKS)]

            await asyncio.gather(*(worker(url) for chunk in chunks for url in chunk))
            return {"parsed_categories": results}
        finally:
            db.close()
```

## threading
```python

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import threading
from math import ceil
import requests
from bs4 import BeautifulSoup

from app.dependencies import get_db
from app.crud import crud_category
from app.schemas.category import CategoryCreate

app = FastAPI(title="Threading Parser API")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

class ParseRequest(BaseModel):
    urls: List[str]

def fetch_title(url: str) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        t = soup.find("title")
        return t.get_text(strip=True) if t else None
    except Exception as e:
        print(f"[THREAD] Error fetching {url}: {e}")
        return None

def worker(urls_chunk, db, results):
    for url in urls_chunk:
        title = fetch_title(url)
        if title:
            cat_data = CategoryCreate(name=title)
            category = crud_category.upsert_category(db, cat_data)
            results.append(category.name)

def chunked(lst, n):
    k = ceil(len(lst) / n)
    return [lst[i * k:(i + 1) * k] for i in range(n)]

@app.post("/parse")
def parse(request: ParseRequest):
    db = next(get_db())
    try:
        results = []
        NUM_THREADS = 3
        chunks = chunked(request.urls, NUM_THREADS)
        threads = []

        for ch in chunks:
            t = threading.Thread(target=worker, args=(ch, db, results))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return {"parsed_categories": results}
    finally:
        db.close()
```

## multiprocessing
```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from multiprocessing import Process, Manager
from math import ceil
import requests
from bs4 import BeautifulSoup

from app.dependencies import get_db
from app.crud import crud_category
from app.schemas.category import CategoryCreate

app = FastAPI(title="Multiprocessing Parser API")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

class ParseRequest(BaseModel):
    urls: List[str]

def fetch_title(url: str) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        t = soup.find("title")
        return t.get_text(strip=True) if t else None
    except Exception as e:
        print(f"[PROCESS] Error fetching {url}: {e}")
        return None

def worker(urls_chunk, results):
    db = next(get_db())
    try:
        for url in urls_chunk:
            title = fetch_title(url)
            if title:
                cat_data = CategoryCreate(name=title)
                category = crud_category.upsert_category(db, cat_data)
                results.append(category.name)
    finally:
        db.close()

def chunked(lst, n):
    k = ceil(len(lst) / n)
    return [lst[i * k:(i + 1) * k] for i in range(n)]

@app.post("/parse")
def parse(request: ParseRequest):
    manager = Manager()
    results = manager.list()
    NUM_PROCESSES = 3
    chunks = chunked(request.urls, NUM_PROCESSES)
    processes = []

    for ch in chunks:
        p = Process(target=worker, args=(ch, results))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return {"parsed_categories": list(results)}
```