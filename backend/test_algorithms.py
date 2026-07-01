"""
PyTest suite for algorithms.py

Run with: pytest -v
Covers: empty array, single element, already sorted, reverse sorted,
duplicates, and correctness against Python's built-in sort/search.
"""
import pytest
from algorithms import (
    bubble_sort,
    merge_sort,
    quick_sort,
    linear_search,
    binary_search,
)

SORT_FUNCTIONS = [bubble_sort, merge_sort, quick_sort]

EDGE_CASES = [
    ([], []),
    ([1], [1]),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),          # already sorted
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),          # reverse sorted
    ([3, 1, 2, 3, 1], [1, 1, 2, 3, 3]),          # duplicates
    ([-5, 10, 0, -3, 7], [-5, -3, 0, 7, 10]),    # negative numbers
]


@pytest.mark.parametrize("sort_fn", SORT_FUNCTIONS)
@pytest.mark.parametrize("input_arr,expected", EDGE_CASES)
def test_sort_correctness(sort_fn, input_arr, expected):
    outcome = sort_fn(input_arr)
    assert outcome["result"] == expected


@pytest.mark.parametrize("sort_fn", SORT_FUNCTIONS)
def test_sort_does_not_mutate_input(sort_fn):
    original = [3, 1, 2]
    original_copy = original.copy()
    sort_fn(original)
    assert original == original_copy, "Algorithm must not mutate the input array"


@pytest.mark.parametrize("sort_fn", SORT_FUNCTIONS)
def test_sort_returns_metrics(sort_fn):
    outcome = sort_fn([5, 3, 8, 1])
    assert "comparisons" in outcome
    assert "time_ms" in outcome
    assert outcome["comparisons"] >= 0


def test_linear_search_found():
    outcome = linear_search([4, 2, 7, 1, 9], 7)
    assert outcome["result"] == 2


def test_linear_search_not_found():
    outcome = linear_search([4, 2, 7, 1, 9], 100)
    assert outcome["result"] == -1


def test_linear_search_empty_array():
    outcome = linear_search([], 5)
    assert outcome["result"] == -1


def test_binary_search_found():
    outcome = binary_search([1, 2, 3, 4, 5, 6, 7], 5)
    assert outcome["result"] != -1
    # value at the returned index must equal the target
    sorted_arr = sorted([1, 2, 3, 4, 5, 6, 7])
    assert sorted_arr[outcome["result"]] == 5


def test_binary_search_not_found():
    outcome = binary_search([1, 3, 5, 7, 9], 4)
    assert outcome["result"] == -1


def test_binary_search_unsorted_input_is_handled():
    # binary_search sorts internally before searching
    outcome = binary_search([9, 1, 5, 3, 7], 5)
    assert outcome["result"] != -1


def test_binary_search_empty_array():
    outcome = binary_search([], 5)
    assert outcome["result"] == -1
