"""
Sorting and searching algorithm implementations.

Each function returns a dict with:
- result: the sorted array / found index
- comparisons: number of element comparisons made
- swaps: number of swaps made (sorting only)
- steps: list of array snapshots, useful for frontend visualization
"""
import time
from typing import List, Dict, Any


def _timed(fn):
    """Wrap an algorithm function to record wall-clock execution time (ms)."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 4)
        result["time_ms"] = elapsed_ms
        return result
    return wrapper


@_timed
def bubble_sort(arr: List[float]) -> Dict[str, Any]:
    a = arr.copy()
    comparisons = 0
    swaps = 0
    steps = [a.copy()]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
                steps.append(a.copy())
        if not swapped:
            break
    return {"result": a, "comparisons": comparisons, "swaps": swaps, "steps": steps}


@_timed
def merge_sort(arr: List[float]) -> Dict[str, Any]:
    comparisons = 0
    steps = []

    def _merge_sort(a: List[float]) -> List[float]:
        nonlocal comparisons
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _merge_sort(a[:mid])
        right = _merge_sort(a[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        steps.append(merged.copy())
        return merged

    result = _merge_sort(arr.copy())
    return {"result": result, "comparisons": comparisons, "swaps": None, "steps": steps}


@_timed
def quick_sort(arr: List[float]) -> Dict[str, Any]:
    a = arr.copy()
    comparisons = 0
    swaps = 0
    steps = [a.copy()]

    def _partition(low: int, high: int) -> int:
        nonlocal comparisons, swaps
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps += 1
                steps.append(a.copy())
        a[i + 1], a[high] = a[high], a[i + 1]
        swaps += 1
        steps.append(a.copy())
        return i + 1

    def _quick_sort(low: int, high: int) -> None:
        if low < high:
            pi = _partition(low, high)
            _quick_sort(low, pi - 1)
            _quick_sort(pi + 1, high)

    if len(a) > 1:
        _quick_sort(0, len(a) - 1)
    return {"result": a, "comparisons": comparisons, "swaps": swaps, "steps": steps}


@_timed
def linear_search(arr: List[float], target: float) -> Dict[str, Any]:
    comparisons = 0
    for idx, val in enumerate(arr):
        comparisons += 1
        if val == target:
            return {"result": idx, "comparisons": comparisons, "swaps": None, "steps": []}
    return {"result": -1, "comparisons": comparisons, "swaps": None, "steps": []}


@_timed
def binary_search(arr: List[float], target: float) -> Dict[str, Any]:
    a = sorted(arr)
    comparisons = 0
    low, high = 0, len(a) - 1
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if a[mid] == target:
            return {"result": mid, "comparisons": comparisons, "swaps": None, "steps": []}
        elif a[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return {"result": -1, "comparisons": comparisons, "swaps": None, "steps": []}


SORT_ALGORITHMS = {
    "bubble": bubble_sort,
    "merge": merge_sort,
    "quick": quick_sort,
}

SEARCH_ALGORITHMS = {
    "linear": linear_search,
    "binary": binary_search,
}
