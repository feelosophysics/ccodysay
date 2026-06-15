"""
sorting.py — 정렬 알고리즘 모듈
=================================

이 모듈은 두 가지 정렬 알고리즘을 직접 구현합니다:

1. 머지 정렬 (Merge Sort)  — 안정 정렬, O(n log n) 보장
2. 퀵 정렬 (Quick Sort)    — 불안정 정렬, 평균 O(n log n), 최악 O(n²)

그리고 보너스 과제 5.3을 위한 성능 비교 함수도 포함합니다.

════════════════════════════════════════════
★ 미션 제약: sorted()와 list.sort() 사용 금지 ★
════════════════════════════════════════════
"""

import time
import hashlib
from typing import List, Callable, Any, Optional
from minigit.constants import SystemMessages


def merge_sort(arr: List[Any], key_func: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    """
    머지 정렬(Merge Sort)을 수행합니다.
    """
    if key_func is None:
        def identity(x: Any) -> Any:
            return x
        key_func = identity

    if len(arr) <= 1:
        return arr[:]

    mid: int = len(arr) // 2
    left: List[Any] = merge_sort(arr[:mid], key_func)
    right: List[Any] = merge_sort(arr[mid:], key_func)

    return _merge(left, right, key_func)


def _merge(left: List[Any], right: List[Any], key_func: Callable[[Any], Any]) -> List[Any]:
    """
    두 정렬된 배열을 하나의 정렬된 배열로 병합합니다.
    """
    result: List[Any] = []
    i: int = 0
    j: int = 0

    while i < len(left) and j < len(right):
        left_key: Any = key_func(left[i])
        right_key: Any = key_func(right[j])

        if left_key <= right_key:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def quick_sort(arr: List[Any], key_func: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    """
    퀵 정렬(Quick Sort)을 수행합니다.
    """
    if key_func is None:
        def identity(x: Any) -> Any:
            return x
        key_func = identity

    if len(arr) <= 1:
        return arr[:]

    pivot: Any = _select_pivot(arr, key_func)
    pivot_key: Any = key_func(pivot)
    
    less: List[Any] = []
    equal: List[Any] = []
    greater: List[Any] = []

    for item in arr:
        item_key: Any = key_func(item)
        if item_key < pivot_key:
            less.append(item)
        elif item_key > pivot_key:
            greater.append(item)
        else:
            equal.append(item)

    return quick_sort(less, key_func) + equal + quick_sort(greater, key_func)


def _select_pivot(arr: List[Any], key_func: Callable[[Any], Any]) -> Any:
    """
    Median-of-Three 전략으로 피벗을 선택합니다.
    """
    if len(arr) <= 2:
        return arr[0]

    first: Any = arr[0]
    mid: Any = arr[len(arr) // 2]
    last: Any = arr[-1]

    f_key: Any = key_func(first)
    m_key: Any = key_func(mid)
    l_key: Any = key_func(last)

    if (f_key <= m_key <= l_key) or (l_key <= m_key <= f_key):
        return mid
    elif (m_key <= f_key <= l_key) or (l_key <= f_key <= m_key):
        return first
    else:
        return last


def benchmark_sorts(n_sizes: Optional[List[int]] = None) -> str:
    """
    [보너스 5.3] 두 정렬 알고리즘의 성능을 비교합니다.
    """
    # ── 1. Data Refinement (데이터 정제) ──
    sizes_to_run: List[int] = []
    if n_sizes is None:
        sizes_to_run = [10, 50, 100, 500, 1000, 3000, 5000]
    else:
        sizes_to_run = n_sizes

    # ── 2. Validation (유효성 검사) ──
    if not sizes_to_run:
        return "No sizes provided for benchmark."

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    lines: List[str] = []
    lines.append(SystemMessages.BENCHMARK_HEADER)

    for n in sizes_to_run:
        data: List[int] = _generate_test_data(n)

        data_copy1: List[int] = data[:]
        start1: float = time.perf_counter()
        merge_sort(data_copy1)
        merge_time: float = time.perf_counter() - start1

        data_copy2: List[int] = data[:]
        start2: float = time.perf_counter()
        quick_sort(data_copy2)
        quick_time: float = time.perf_counter() - start2

        winner: str = ""
        if merge_time < quick_time:
            winner = "Merge"
        elif quick_time < merge_time:
            winner = "Quick"
        else:
            winner = "Tie"

        row: str = SystemMessages.BENCHMARK_ROW.format(
            size=n, 
            merge=merge_time, 
            quick=quick_time, 
            winner=winner
        )
        lines.append(row)

    lines.append(SystemMessages.BENCHMARK_FOOTER)
    return "\n".join(lines)


def _generate_test_data(n: int) -> List[int]:
    """
    벤치마크용 결정적 테스트 데이터를 생성합니다.
    """
    data: List[int] = []
    for i in range(n):
        hash_val: str = hashlib.sha1(str(i).encode()).hexdigest()
        data.append(int(hash_val[:8], 16))
    return data
