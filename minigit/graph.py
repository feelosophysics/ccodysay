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

# 💡 파이썬 현미경 해설
# `collections.deque`는 양쪽 끝에서 넣고 뺄 수 있는 매우 빠른 리스트(큐)입니다.
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
    # 💡 파이썬 현미경 해설
    # `if not commits_dict:` 만약 딕셔너리가 비어있다면, 빈 리스트를 즉시 반환합니다.
    if not commits_dict:
        return []

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    # 💡 파이썬 현미경 해설
    # `in_degree`는 "나를 가리키는 화살표(진입 차수)가 몇 개인지" 세어두는 딕셔너리입니다.
    in_degree: Dict[str, int] = {}
    
    # 💡 파이썬 현미경 해설
    # `for ... in ...:` (for문)은 딕셔너리 안에 있는 것을 처음부터 끝까지 하나씩 꺼내며 반복합니다.
    # 먼저 모든 커밋의 화살표 개수를 0으로 초기화합니다.
    for commit_hash in commits_dict:
        in_degree[commit_hash] = 0

    # 💡 파이썬 현미경 해설
    # `.items()`를 쓰면 딕셔너리에서 이름(키)과 내용(값)을 한꺼번에 꺼낼 수 있습니다.
    for commit_hash, commit in commits_dict.items():
        # 각 커밋이 가리키고 있는 부모들을 찾아가서, 부모의 '진입 차수'를 1씩 올려줍니다.
        for parent_hash in commit.parents:
            if parent_hash in in_degree:
                in_degree[parent_hash] += 1

    # 💡 파이썬 현미경 해설
    # 아무도 나를 가리키지 않는 노드(진입 차수가 0인 노드 = 즉, 최신 커밋)들을 담을 큐를 만듭니다.
    queue: deque[str] = deque()
    for commit_hash, degree in in_degree.items():
        # `==`: 숫자가 같은지 비교
        if degree == 0:
            queue.append(commit_hash)

    result: List[Commit] = []
    
    # 💡 파이썬 현미경 해설
    # `while queue:` 큐 안에 처리할 데이터가 남아있는 동안 계속 반복합니다.
    while queue:
        # `.popleft()`는 큐의 가장 왼쪽(먼저 들어온 것)을 뽑아냅니다.
        current_hash: str = queue.popleft()
        current_commit: Commit = commits_dict[current_hash]
        # 결과 리스트에 차곡차곡 담습니다.
        result.append(current_commit)

        # 방금 빼낸 커밋이 가리키고 있던 부모들의 화살표를 1개씩 지워줍니다.
        for parent_hash in current_commit.parents:
            if parent_hash in in_degree:
                in_degree[parent_hash] -= 1
                # 만약 화살표가 0개가 되었다면(선행 조건이 모두 끝났다면) 큐에 넣습니다!
                if in_degree[parent_hash] == 0:
                    queue.append(parent_hash)

    # 💡 파이썬 현미경 해설
    # `.reverse()`는 리스트의 순서를 완전히 뒤집어줍니다. (과거 -> 최신 순으로 보기 위함)
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
    # `not in` 연산자를 사용해 딕셔너리 안에 이 커밋 해시가 존재하는지 검사합니다.
    if clean_hash1 not in commits_dict or clean_hash2 not in commits_dict:
        return None
    if clean_hash1 == clean_hash2:
        # 💡 파이썬 현미경 해설: 대괄호 `[]`로 문자열 하나를 감싸서 크기가 1인 리스트를 반환합니다.
        return [clean_hash1]

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    # BFS를 위해 단방향 그래프를 "양방향" 인접 리스트(adjacency list)로 변환합니다.
    adjacency: Dict[str, List[str]] = {}
    for commit_hash in commits_dict:
        adjacency[commit_hash] = []

    for commit_hash, commit in commits_dict.items():
        for parent_hash in commit.parents:
            if parent_hash in commits_dict:
                # 💡 파이썬 현미경 해설: `append`로 리스트의 끝에 요소를 추가합니다. (양쪽 모두 추가)
                adjacency[commit_hash].append(parent_hash)
                adjacency[parent_hash].append(commit_hash)

    # 💡 파이썬 현미경 해설
    # `visited`는 이미 방문한 곳을 기록하는 `set`(세트)입니다. 세트는 탐색 속도가 매우 빠릅니다.
    visited: Set[str] = set()
    
    # `parent_map`은 "내가 어디서 왔는지(누가 나를 발견했는지)" 발자취를 기록하는 딕셔너리입니다.
    parent_map: Dict[str, str] = {}
    queue: deque[str] = deque()

    # 시작점을 큐에 넣고, 방문했다고 표시합니다.
    queue.append(clean_hash1)
    visited.add(clean_hash1)
    # `bool`(불리언) 타입. True(참) / False(거짓) 중 하나만 가집니다.
    found: bool = False

    while queue:
        current: str = queue.popleft()
        
        # 💡 파이썬 현미경 해설
        # 찾고자 하는 목표 지점에 도달했다면? `break`를 써서 반복문(while)을 즉시 탈출합니다!
        if current == clean_hash2:
            found = True
            break

        # 내 주변에 연결된 이웃 노드들을 가져옵니다. (없으면 빈 리스트 `[]` 반환)
        neighbors: List[str] = adjacency.get(current, [])
        # 알파벳 순서대로 탐색하기 위해 정렬합니다.
        sorted_neighbors: List[str] = _insertion_sort_strings(neighbors)

        for neighbor in sorted_neighbors:
            # 아직 방문하지 않은 이웃이라면
            if neighbor not in visited:
                visited.add(neighbor)             # 방문 표시!
                parent_map[neighbor] = current    # "이웃아, 널 발견한 건 나(current)야" 하고 기록!
                queue.append(neighbor)            # 다음 탐색 대기열에 추가!

    if not found:
        return None

    # 💡 파이썬 현미경 해설
    # 목표 지점부터 시작해서 거꾸로 발자취(`parent_map`)를 되짚어 오며 경로 리스트를 만듭니다.
    path: List[str] = []
    current_trace: str = clean_hash2
    
    # 시작점에 도달할 때까지 계속 거슬러 올라갑니다 (`!=`는 "다르다"는 뜻입니다)
    while current_trace != clean_hash1:
        path.append(current_trace)
        current_trace = parent_map[current_trace]
        
    path.append(clean_hash1)
    path.reverse()  # 거꾸로 거슬러 왔으므로, 다시 뒤집어주면 올바른 경로가 됩니다.

    return path


def _insertion_sort_strings(arr: List[str]) -> List[str]:
    """
    문자열 배열을 삽입 정렬로 정렬합니다.
    """
    # 💡 파이썬 현미경 해설
    # `arr[:]` : 슬라이싱을 이용해 원본 리스트를 똑같이 복사(얕은 복사)합니다.
    # 원본을 훼손하지 않기 위함입니다.
    result: List[str] = arr[:]
    
    # 💡 파이썬 현미경 해설
    # `range(1, len(result))` : 1부터 (배열 길이 - 1)까지 숫자를 하나씩 만들어냅니다.
    for i in range(1, len(result)):
        key: str = result[i]
        j: int = i - 1
        # 내 앞의 글자들이 나보다 크면, 한 칸씩 뒤로 미룹니다.
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        # 적절한 자리를 찾아 쏙 들어갑니다! (삽입 정렬)
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
    # 💡 파이썬 현미경 해설
    # DFS(깊이 우선 탐색)는 큐 대신 "스택(Stack)"을 사용합니다. 파이썬에서는 그냥 리스트 `[]`를 쓰면 됩니다.
    stack: List[str] = []

    start_commit: Commit = commits_dict[clean_hash]
    for parent_hash in start_commit.parents:
        if parent_hash in commits_dict:
            stack.append(parent_hash)

    while stack:
        # 💡 파이썬 현미경 해설
        # `.pop()`은 리스트의 **맨 마지막** 요소를 뽑아냅니다. (가장 최근에 넣은 것을 먼저 꺼냄 = LIFO)
        current: str = stack.pop()
        
        # 💡 파이썬 현미경 해설
        # `continue`는 "이번 바퀴는 여기서 건너뛰고 바로 다음 바퀴로 넘어가라"는 뜻입니다.
        if current in visited:
            continue

        visited.add(current)
        ancestors.append(current)

        current_commit: Commit = commits_dict[current]
        # 방금 꺼낸 노드의 부모들을 다시 스택에 욱여넣습니다. (점점 깊이 들어갑니다)
        for parent_hash in current_commit.parents:
            if parent_hash in commits_dict and parent_hash not in visited:
                stack.append(parent_hash)

    return ancestors
