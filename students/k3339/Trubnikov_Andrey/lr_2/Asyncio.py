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

'''
Результат 
Asyncio result: 500000000500000000
Execution time: 6.63 seconds
'''