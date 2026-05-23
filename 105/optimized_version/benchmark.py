import time
from algorithms import binary_search

products = [f"Product{i}" for i in range(100)]
products.sort()

query = "Product99"


# ─────────────────────────────
# BASELINE — LINEAR SEARCH
# ─────────────────────────────
start = time.perf_counter()

results = binary_search(products, query)

end = time.perf_counter()

optimized_time = (end - start) * 1_000_000

print(f"Optimized Binary Search: {optimized_time:.2f} microseconds")
