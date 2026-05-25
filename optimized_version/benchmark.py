import time

from algorithms import binary_search


def linear_search(products, query):
    query = query.lower()
    return [name for name in products if name.lower().startswith(query)]


def time_call(fn, repetitions):
    start = time.perf_counter()
    result = None
    for _ in range(repetitions):
        result = fn()
    elapsed = (time.perf_counter() - start) * 1_000_000
    return elapsed / repetitions, result


def run_benchmark(input_size=10_000, repetitions=1_000):
    products = [f"Product{i:05d}" for i in range(input_size)]
    products.sort()
    query = f"Product{input_size - 1:05d}"

    baseline_time, baseline_result = time_call(
        lambda: linear_search(products, query), repetitions)
    optimized_time, optimized_result = time_call(
        lambda: binary_search(products, query), repetitions)

    if baseline_result != optimized_result:
        raise RuntimeError("Benchmark mismatch: baseline and optimized results differ.")

    improvement = 0.0
    if baseline_time:
        improvement = ((baseline_time - optimized_time) / baseline_time) * 100

    print(f"Input size: {input_size}")
    print(f"Repetitions: {repetitions}")
    print(f"Query: {query}")
    print(f"Baseline linear search: {baseline_time:.2f} microseconds")
    print(f"Optimized binary search: {optimized_time:.2f} microseconds")
    print(f"Improvement: {improvement:.2f}%")


if __name__ == "__main__":
    run_benchmark()
