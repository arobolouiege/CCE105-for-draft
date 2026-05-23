# ─────────────────────────────────────────────────────────────
# algorithms.py — Core DSA Implementations
# Aligns with Deliverable I: Smart Sari-Sari Store
# Algorithms: Hash Table, Binary Search, Merge Sort,
#              Priority Queue (Heap), Dijkstra's Algorithm
# ─────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
# 1. HASH TABLE — O(1) average product lookup
# ══════════════════════════════════════════════════════════════

class HashTable:
    """
    Separate-chaining hash table for O(1) product lookup.
    Keys: product names (str). Values: product dicts.
    """

    def __init__(self, capacity: int = 64):
        self._cap   = capacity
        self._buckets: list[list] = [[] for _ in range(capacity)]
        self._size  = 0

    def _hash(self, key: str) -> int:
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % self._cap
        return h

    def insert(self, key: str, value) -> None:
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._buckets[idx]):
            if k == key:
                self._buckets[idx][i] = (key, value)
                return
        self._buckets[idx].append((key, value))
        self._size += 1

    def get(self, key: str):
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key: str) -> bool:
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._buckets[idx]):
            if k == key:
                del self._buckets[idx][i]
                self._size -= 1
                return True
        return False

    def all_values(self) -> list:
        result = []
        for bucket in self._buckets:
            for _, v in bucket:
                result.append(v)
        return result

    def all_keys(self) -> list:
        result = []
        for bucket in self._buckets:
            for k, _ in bucket:
                result.append(k)
        return result

    def __len__(self) -> int:
        return self._size

    def load_products(self, rows: list[dict]) -> None:
        """Bulk-load product rows from DB into the hash table."""
        for r in rows:
            self.insert(r["product_name"], r)


# ══════════════════════════════════════════════════════════════
# 2. BINARY SEARCH — O(log n) sorted-list search
# ══════════════════════════════════════════════════════════════

def binary_search(sorted_items: list, query: str) -> list:
    """
    Case-insensitive prefix binary search on a sorted list of
    product-name strings. Returns all matching names.
    O(log n) to find the first match, then O(k) for k results.
    """
    query = query.lower()
    lo, hi = 0, len(sorted_items) - 1
    start  = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_items[mid].lower() >= query:
            start = mid
            hi    = mid - 1
        else:
            lo    = mid + 1

    if start == -1:
        return []

    results = []
    for i in range(start, len(sorted_items)):
        if sorted_items[i].lower().startswith(query):
            results.append(sorted_items[i])
        elif sorted_items[i].lower() > query and not sorted_items[i].lower().startswith(query):
            break
    return results


# ══════════════════════════════════════════════════════════════
# 3. MERGE SORT — O(n log n) sales / stock ranking
# ══════════════════════════════════════════════════════════════

def merge_sort(items: list, key=lambda x: x, reverse: bool = False) -> list:
    """
    Pure merge-sort.  key: callable that extracts the sort value.
    Stable, O(n log n).
    """
    if len(items) <= 1:
        return items[:]

    mid   = len(items) // 2
    left  = merge_sort(items[:mid],  key, reverse)
    right = merge_sort(items[mid:],  key, reverse)

    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        lv, rv = key(left[i]), key(right[j])
        if (lv >= rv) if reverse else (lv <= rv):
            merged.append(left[i]);  i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ══════════════════════════════════════════════════════════════
# 4. MIN-HEAP PRIORITY QUEUE — O(log n) restock prioritisation
# ══════════════════════════════════════════════════════════════

class MinHeap:
    """
    Min-heap where priority = stock_qty / reorder_level ratio.
    Lower ratio → higher urgency → comes out first.
    """

    def __init__(self):
        self._data: list[tuple] = []   # (priority, item_dict)

    # ── Internal helpers ─────────────────────────────────────
    def _parent(self, i):  return (i - 1) // 2
    def _left(self, i):    return 2 * i + 1
    def _right(self, i):   return 2 * i + 2

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _sift_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self._data[i][0] < self._data[p][0]:
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            smallest, l, r = i, self._left(i), self._right(i)
            if l < n and self._data[l][0] < self._data[smallest][0]:
                smallest = l
            if r < n and self._data[r][0] < self._data[smallest][0]:
                smallest = r
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    # ── Public API ───────────────────────────────────────────
    def push(self, priority: float, item: dict) -> None:
        self._data.append((priority, item))
        self._sift_up(len(self._data) - 1)

    def pop(self) -> tuple:
        if not self._data:
            raise IndexError("Heap is empty")
        self._swap(0, len(self._data) - 1)
        top = self._data.pop()
        if self._data:
            self._sift_down(0)
        return top

    def peek(self) -> tuple:
        return self._data[0] if self._data else None

    def __len__(self) -> int:
        return len(self._data)

    def to_sorted_list(self) -> list[dict]:
        """Drain a copy and return items in priority order."""
        import copy
        clone = MinHeap()
        clone._data = copy.deepcopy(self._data)
        result = []
        while len(clone):
            _, item = clone.pop()
            result.append(item)
        return result

    @classmethod
    def build_restock_queue(cls, products: list[dict]) -> "MinHeap":
        """
        Build a restock priority queue.
        Priority = stock_qty / reorder_level  (lower = more urgent).
        Products with stock == 0 get priority 0.0.
        """
        heap = cls()
        for p in products:
            reorder = max(p.get("reorder_level", 1), 1)
            stock   = max(int(p.get("stock_qty", 0)), 0)
            priority = stock / reorder
            heap.push(priority, p)
        return heap


# ══════════════════════════════════════════════════════════════
# 5. DIJKSTRA'S ALGORITHM — optimal supplier selection
# ══════════════════════════════════════════════════════════════

class SupplierGraph:
    """
    Weighted undirected graph of suppliers + a virtual 'store' node.
    Edge weight = composite score: distance_km * 0.5 + price_index * 0.5
    Dijkstra finds the cheapest-nearest supplier for a product.
    """

    def __init__(self):
        # adjacency list: node -> [(neighbour, weight)]
        self._adj: dict[str, list[tuple]] = {}

    def add_node(self, name: str) -> None:
        if name not in self._adj:
            self._adj[name] = []

    def add_edge(self, u: str, v: str, weight: float) -> None:
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, weight))
        self._adj[v].append((u, weight))

    def dijkstra(self, source: str) -> dict[str, float]:
        """
        Returns dict of {node: shortest_distance_from_source}.
        O((V + E) log V) via a binary-heap priority queue.
        """
        import math
        dist = {n: math.inf for n in self._adj}
        dist[source] = 0.0
        heap = MinHeap()
        heap.push(0.0, {"node": source})

        while len(heap):
            d, item = heap.pop()
            node = item["node"]
            if d > dist[node]:
                continue
            for neighbour, w in self._adj.get(node, []):
                nd = dist[node] + w
                if nd < dist[neighbour]:
                    dist[neighbour] = nd
                    heap.push(nd, {"node": neighbour})
        return dist

    def best_supplier(self, source: str,
                      supplier_names: list[str]) -> list[tuple]:
        """
        Returns suppliers ranked by total cost (distance + price index)
        from source node.  List of (supplier_name, score).
        """
        dist = self.dijkstra(source)
        ranked = [(s, dist.get(s, float("inf"))) for s in supplier_names]
        return merge_sort(ranked, key=lambda x: x[1])

    @classmethod
    def build_from_suppliers(cls, suppliers: list[dict],
                              store_node: str = "Store") -> "SupplierGraph":
        """
        Build a fully-connected graph from supplier dicts.
        Each supplier dict must have 'supplier_name', 'distance_km',
        'price_index' (1–10 scale, lower = cheaper).
        The store connects to every supplier directly.
        Suppliers are also cross-connected for completeness.
        """
        g = cls()
        g.add_node(store_node)

        for sup in suppliers:
            name = sup["supplier_name"]
            dist = float(sup.get("distance_km", 5.0))
            pi   = float(sup.get("price_index", 5.0))
            weight = dist * 0.5 + pi * 0.5
            g.add_edge(store_node, name, weight)

        # cross-connect suppliers (simulate supplier network)
        import math
        for i, a in enumerate(suppliers):
            for b in suppliers[i + 1:]:
                d = abs(float(a.get("distance_km", 5)) -
                        float(b.get("distance_km", 5))) + 1
                g.add_edge(a["supplier_name"], b["supplier_name"], d)

        return g
