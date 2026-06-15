"""
graph.py — 그래프 알고리즘 모듈
================================

이 모듈은 커밋 DAG(방향성 비순환 그래프)에서 수행되는
세 가지 핵심 그래프 알고리즘을 구현합니다:

1. 위상 정렬 (Topological Sort)  — Kahn's Algorithm
2. 최단 경로 탐색 (Shortest Path) — BFS (너비 우선 탐색)
3. 조상 탐색 (Ancestor Search)    — DFS (깊이 우선 탐색)

────────────────────────────────────────────
그래프 알고리즘과 Git의 관계
────────────────────────────────────────────
Git의 커밋 히스토리는 DAG입니다. 이 DAG 위에서:
- `git log`     → 위상 정렬 (부모가 먼저 출력)
- `git log --ancestry-path` → BFS/DFS로 경로 탐색
- `git merge-base` → 공통 조상 탐색 (BFS/DFS)

우리가 구현하는 세 알고리즘은 이런 Git 내부 연산의 기초입니다.

────────────────────────────────────────────
BFS vs DFS — 언제 어떤 것을 쓰는가?
────────────────────────────────────────────
■ BFS (너비 우선 탐색):
  - 시작점에서 가까운 노드부터 방문합니다.
  - 무가중치 그래프에서 최단 경로를 보장합니다.
  - 큐(Queue)를 사용합니다.
  - 공간복잡도: O(V) (최악의 경우 한 레벨의 모든 노드를 큐에 저장)

■ DFS (깊이 우선 탐색):
  - 한 방향으로 끝까지 깊이 들어간 후 되돌아옵니다.
  - 모든 경로를 탐색하거나, 연결 요소를 찾을 때 적합합니다.
  - 스택(Stack) 또는 재귀를 사용합니다.
  - 공간복잡도: O(V) (최악의 경우 경로의 모든 노드를 스택에 저장)

두 알고리즘 모두 시간복잡도는 O(V + E)입니다.
(V = 정점 수, E = 간선 수)
"""

from collections import deque
from typing import Dict, List, Optional, Set
from minigit.models import Commit


def topological_sort(commits_dict: Dict[str, Commit]) -> List[Commit]:
    """
    Kahn's Algorithm으로 커밋 그래프의 위상 정렬을 수행합니다.

    ── 위상 정렬(Topological Sort)이란? ──
    DAG의 모든 노드를, "모든 간선이 앞에서 뒤를 가리키도록" 일렬로 나열하는 것입니다.
    즉, 노드 A에서 노드 B로 가는 간선이 있으면, A는 반드시 B보다 앞에 옵니다.
    """
    # ── 1. Data Refinement (데이터 정제) ──
    # 이 함수는 정제할 입력 데이터가 단순 딕셔너리이므로 패스합니다.

    # ── 2. Validation (유효성 검사) ──
    if not commits_dict:
        return []

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    in_degree: Dict[str, int] = {}
    for commit_hash in commits_dict:
        in_degree[commit_hash] = 0

    for commit_hash, commit in commits_dict.items():
        for parent_hash in commit.parents:
            if parent_hash in in_degree:
                in_degree[parent_hash] += 1

    queue: deque[str] = deque()
    for commit_hash, degree in in_degree.items():
        if degree == 0:
            queue.append(commit_hash)

    result: List[Commit] = []
    while queue:
        current_hash: str = queue.popleft()
        current_commit: Commit = commits_dict[current_hash]
        result.append(current_commit)

        for parent_hash in current_commit.parents:
            if parent_hash in in_degree:
                in_degree[parent_hash] -= 1
                if in_degree[parent_hash] == 0:
                    queue.append(parent_hash)

    result.reverse()
    return result


def find_shortest_path(commits_dict: Dict[str, Commit], hash1: str, hash2: str) -> Optional[List[str]]:
    """
    두 커밋 사이의 최단 경로를 BFS로 찾습니다.
    """
    # ── 1. Data Refinement (데이터 정제) ──
    clean_hash1: str = hash1.strip()
    clean_hash2: str = hash2.strip()

    # ── 2. Validation (유효성 검사) ──
    if clean_hash1 not in commits_dict or clean_hash2 not in commits_dict:
        return None
    if clean_hash1 == clean_hash2:
        return [clean_hash1]

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    adjacency: Dict[str, List[str]] = {}
    for commit_hash in commits_dict:
        adjacency[commit_hash] = []

    for commit_hash, commit in commits_dict.items():
        for parent_hash in commit.parents:
            if parent_hash in commits_dict:
                adjacency[commit_hash].append(parent_hash)
                adjacency[parent_hash].append(commit_hash)

    visited: Set[str] = set()
    parent_map: Dict[str, str] = {}
    queue: deque[str] = deque()

    queue.append(clean_hash1)
    visited.add(clean_hash1)
    found: bool = False

    while queue:
        current: str = queue.popleft()
        if current == clean_hash2:
            found = True
            break

        neighbors: List[str] = adjacency.get(current, [])
        sorted_neighbors: List[str] = _insertion_sort_strings(neighbors)

        for neighbor in sorted_neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current
                queue.append(neighbor)

    if not found:
        return None

    path: List[str] = []
    current_trace: str = clean_hash2
    while current_trace != clean_hash1:
        path.append(current_trace)
        current_trace = parent_map[current_trace]
    path.append(clean_hash1)
    path.reverse()

    return path


def _insertion_sort_strings(arr: List[str]) -> List[str]:
    """
    문자열 배열을 삽입 정렬로 정렬합니다.
    """
    result: List[str] = arr[:]
    for i in range(1, len(result)):
        key: str = result[i]
        j: int = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def find_ancestors(commits_dict: Dict[str, Commit], commit_hash: str) -> List[str]:
    """
    특정 커밋의 모든 조상을 DFS로 찾습니다.
    """
    # ── 1. Data Refinement (데이터 정제) ──
    clean_hash: str = commit_hash.strip()

    # ── 2. Validation (유효성 검사) ──
    if clean_hash not in commits_dict:
        return []

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    ancestors: List[str] = []
    visited: Set[str] = set()
    stack: List[str] = []

    start_commit: Commit = commits_dict[clean_hash]
    for parent_hash in start_commit.parents:
        if parent_hash in commits_dict:
            stack.append(parent_hash)

    while stack:
        current: str = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        ancestors.append(current)

        current_commit: Commit = commits_dict[current]
        for parent_hash in current_commit.parents:
            if parent_hash in commits_dict and parent_hash not in visited:
                stack.append(parent_hash)

    return ancestors
