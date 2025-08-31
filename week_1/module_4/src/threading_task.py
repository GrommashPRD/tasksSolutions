import json
import multiprocessing
import random
import time
from concurrent.futures import ProcessPoolExecutor

# TODO \
# Разработайте программу, которая выполняет следующие шаги:\
# Сбор данных:\
# Создайте функцию generate_data(n), которая генерирует список из n случайных целых чисел в диапазоне от 1 до 1000. \
# Например, generate_data(1000000) должна вернуть список из 1 миллиона случайных чисел.\
# Обработка данных:\
# Напишите функцию process_number(number), которая выполняет вычисления над числом. \
# Например, вычисляет факториал числа или проверяет, является ли число простым. \
# Обратите внимание, что обработка должна быть ресурсоёмкой, чтобы продемонстрировать преимущества мультипроцессинга.\
# Параллельная обработка:\
# Используйте модули multiprocessing и concurrent.futures для параллельной обработки списка чисел.\
# Реализуйте три варианта:\
# Вариант А: Ипользование пула потоков с concurrent.futures.\
# Вариант Б: Использование multiprocessing.Pool с пулом процессов, равным количеству CPU.\
# Вариант В: Создание отдельных процессов с использованием multiprocessing.Process \
# и очередей (multiprocessing.Queue) для передачи данных.\
# Сравнение производительности:\
# Измерьте время выполнения для всех вариантов и сравните их с \
# однопоточным (однопроцессным) вариантом. Представьте результаты в виде таблицы или графика.\
# Сохранение результатов:\
# Сохраните обработанные данные в файл (например, в формате JSON или CSV).


def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


def process_with_concurrent(data):
    with ProcessPoolExecutor() as executor:
        start = time.time()
        results = list(executor.map(process_number, data))
        end = time.time()
    return results, end - start


def process_with_pool(data):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        start = time.time()
        results = pool.map(process_number, data)
        end = time.time()
    return results, end - start


def worker(input_queue, output_queue):
    while True:
        number = input_queue.get()
        if number is None:
            break
        result = process_number(number)
        output_queue.put((number, result))


def process_with_processes(data):
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    start = time.time()
    for number in data:
        input_queue.put(number)

    for _ in processes:
        input_queue.put(None)

    results = {}
    for _ in range(len(data)):
        number, result = output_queue.get()
        results[number] = result

    for p in processes:
        p.join()

    end = time.time()
    return results, end - start


def process_single_thread(data):
    start = time.time()
    results = [process_number(num) for num in data]
    end = time.time()
    return results, end - start


def main():
    data = generate_data(1000000)

    results = {
        "single_thread": process_single_thread(data),
        "concurrent": process_with_concurrent(data),
        "pool": process_with_pool(data),
        "processes": process_with_processes(data),
    }

    print("\nРезультаты обработки:")
    for method, (res, time) in results.items():
        print(f"{method}: {time:.2f} секунд")

    with open("./results.json", "w") as f:
        json.dump({"execution_times": {k: v[1] for k, v in results.items()}}, f)


if __name__ == "__main__":
    main()
