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
# 💡 파이썬 현미경 해설
# `Callable`: 함수 자체를 변수에 담아서 전달할 때 쓰는 타입 힌트입니다.
# `Any`: 어떤 타입이든 들어올 수 있다는 뜻입니다. (정수, 문자열, 커밋 객체 등)
from typing import List, Callable, Any, Optional
from minigit.constants import SystemMessages


# 💡 파이썬 현미경 해설
# `key_func`는 정렬의 '기준'을 정해주는 함수입니다.
# 예를 들어, 학생 리스트가 있을 때 "이름순"으로 정렬할지 "점수순"으로 정렬할지 알려주는 도구입니다.
def merge_sort(arr: List[Any], key_func: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    """
    머지 정렬(Merge Sort)을 수행합니다.
    """
    if key_func is None:
        # 💡 파이썬 현미경 해설
        # 만약 기준 함수가 안 주어졌다면, 그냥 들어온 값 그대로를 반환하는 `identity` 함수를 임시로 만듭니다.
        def identity(x: Any) -> Any:
            return x
        key_func = identity

    # 💡 파이썬 현미경 해설
    # 배열의 길이가 1개 이하(0개 또는 1개)면 이미 정렬된 상태이므로, 그대로 복사해서 돌려줍니다.
    if len(arr) <= 1:
        return arr[:]

    # 💡 파이썬 현미경 해설
    # `//`: 나눗셈을 하되 소수점을 버리고 정수 몫만 구하는 연산자입니다. (배열을 반으로 쪼갭니다)
    mid: int = len(arr) // 2
    
    # 💡 파이썬 현미경 해설
    # 재귀 호출(자기 자신을 다시 부름)!
    # 왼쪽 절반(`arr[:mid]`)을 다시 머지 정렬하고, 오른쪽 절반(`arr[mid:]`)을 다시 머지 정렬합니다.
    left: List[Any] = merge_sort(arr[:mid], key_func)
    right: List[Any] = merge_sort(arr[mid:], key_func)

    # 쪼개진 걸 다 정렬했으니, 이제 하나로 합칩니다!
    return _merge(left, right, key_func)


def _merge(left: List[Any], right: List[Any], key_func: Callable[[Any], Any]) -> List[Any]:
    """
    두 정렬된 배열을 하나의 정렬된 배열로 병합합니다.
    """
    result: List[Any] = []
    i: int = 0  # 왼쪽 배열을 가리키는 손가락
    j: int = 0  # 오른쪽 배열을 가리키는 손가락

    # 💡 파이썬 현미경 해설
    # 두 손가락 중 하나라도 끝에 도달하기 전까지 계속 비교합니다.
    while i < len(left) and j < len(right):
        left_key: Any = key_func(left[i])
        right_key: Any = key_func(right[j])

        # 왼쪽 값이 더 작거나 같으면, 왼쪽 값을 결과 주머니에 넣고 왼쪽 손가락을 다음 칸으로 넘깁니다.
        if left_key <= right_key:
            result.append(left[i])
            i += 1
        # 오른쪽 값이 더 작으면 오른쪽 값을 주머니에 넣습니다.
        else:
            result.append(right[j])
            j += 1

    # 💡 파이썬 현미경 해설
    # 어느 한쪽이 먼저 끝났다면, 남은 쪽의 나머지 요소들을 몽땅 주머니에 쓸어 담습니다.
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

    # 💡 파이썬 현미경 해설
    # 퀵 정렬의 핵심! 기준점(Pivot)을 잡습니다.
    pivot: Any = _select_pivot(arr, key_func)
    pivot_key: Any = key_func(pivot)
    
    less: List[Any] = []    # 피벗보다 작은 애들
    equal: List[Any] = []   # 피벗이랑 같은 애들
    greater: List[Any] = [] # 피벗보다 큰 애들

    for item in arr:
        item_key: Any = key_func(item)
        if item_key < pivot_key:
            less.append(item)
        elif item_key > pivot_key:
            greater.append(item)
        else:
            equal.append(item)

    # 💡 파이썬 현미경 해설
    # 작은 애들끼리 다시 퀵 정렬, 큰 애들끼리 다시 퀵 정렬한 뒤,
    # (작은애들) + (같은애들) + (큰애들) 순서로 리스트를 이어 붙여(+) 반환합니다.
    return quick_sort(less, key_func) + equal + quick_sort(greater, key_func)


def _select_pivot(arr: List[Any], key_func: Callable[[Any], Any]) -> Any:
    """
    Median-of-Three 전략으로 피벗을 선택합니다.
    (맨 앞, 맨 뒤, 중간 값 3개 중 중간 크기를 가진 것을 피벗으로 골라 성능 저하를 방지합니다)
    """
    if len(arr) <= 2:
        return arr[0]

    first: Any = arr[0]             # 맨 앞
    mid: Any = arr[len(arr) // 2]   # 한가운데
    last: Any = arr[-1]             # 맨 끝 (-1 인덱스는 파이썬에서 리스트의 맨 마지막을 의미합니다)

    f_key: Any = key_func(first)
    m_key: Any = key_func(mid)
    l_key: Any = key_func(last)

    # 💡 파이썬 현미경 해설
    # `(A <= B <= C)`처럼 파이썬에서는 수학식처럼 두 번 비교를 한 줄에 쓸 수 있습니다!
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
        # 💡 파이썬 현미경 해설
        # `time.perf_counter()`는 성능 측정을 위한 아주 정밀한 시계입니다.
        # 시작 전 시간을 기록하고, 끝난 뒤 다시 시간을 재서 빼면 걸린 시간이 나옵니다.
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
        # 💡 파이썬 현미경 해설
        # `int(..., 16)`은 문자열(hex)을 16진수 숫자로 인식해서 정수로 바꿔주는 마법입니다.
        data.append(int(hash_val[:8], 16))
    return data
