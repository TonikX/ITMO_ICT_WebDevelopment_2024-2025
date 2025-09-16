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


'''
Результат 
Threading result: 500000000500000000
Execution time: 21.58 seconds
'''
