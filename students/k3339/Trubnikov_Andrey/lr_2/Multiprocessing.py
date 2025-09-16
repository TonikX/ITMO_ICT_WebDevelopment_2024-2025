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

'''
Результат 
Multiprocessing result: 500000000500000000
Execution time: 5.89 seconds
'''
