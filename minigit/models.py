"""
models.py — Mini Git 핵심 데이터 모델
=====================================

이 모듈은 Mini Git의 두 가지 핵심 클래스를 정의합니다:

1. Commit  — 하나의 커밋을 표현하는 노드 (DAG의 정점)
2. Repository — 저장소 전체 상태를 관리하는 컨트롤러

────────────────────────────────────────────
왜 DAG(Directed Acyclic Graph)인가?
────────────────────────────────────────────
Git의 커밋 그래프는 DAG입니다.
- "방향성(Directed)":  각 커밋은 자신의 부모(parent)를 가리킵니다.
                       즉, 간선의 방향이 자식 → 부모입니다.
- "비순환(Acyclic)":   커밋 A → B → C → A 같은 순환이 불가능합니다.
                       왜냐하면 커밋은 항상 이미 존재하는 커밋만 부모로 가질 수 있기 때문입니다.
                       미래의 커밋을 부모로 지정할 수 없으므로, 순환이 구조적으로 불가능합니다.

이 구조 덕분에:
- 위상 정렬(topological sort)이 가능하고,
- 두 커밋의 공통 조상(merge-base)을 찾을 수 있으며,
- rebase, cherry-pick 같은 고급 연산의 기반이 됩니다.

────────────────────────────────────────────
해시(Hash)의 역할
────────────────────────────────────────────
실제 Git은 커밋 내용(트리, 부모, 작성자, 메시지 등)을
SHA-1으로 해싱하여 40자리 hex 문자열을 만듭니다.
이 해시가 커밋의 고유 식별자(ID)가 됩니다.

우리 Mini Git도 동일한 원리를 사용하되,
가독성을 위해 앞 6자리만 사용합니다.
만약 6자리가 충돌(collision)하면, 내부 카운터를 붙여 유일성을 보장합니다.
"""

import hashlib
import time
from typing import Dict, List, Optional, Set
from minigit.index import InvertedIndex
from minigit.constants import ErrorMessages, SystemMessages, ConfigConstants


class Commit:
    """
    커밋 노드를 표현하는 클래스.

    실제 Git에서 하나의 커밋 객체는 다음 정보를 담고 있습니다:
    - tree:    해당 시점의 파일 상태 스냅샷 (우리는 파일 추적을 하지 않으므로 생략)
    - parent:  이전 커밋(들)의 해시 (0개: 최초 커밋, 1개: 일반 커밋, 2개: 머지 커밋)
    - author:  작성자 이름
    - message: 커밋 메시지
    - timestamp: 커밋 시간

    이 클래스는 위의 정보 중 우리에게 필요한 것만 구현합니다.

    Attributes:
        hash (str):        커밋의 고유 식별자 (SHA-1 앞 6자리 hex)
        message (str):     커밋 메시지 (예: "Add login feature")
        author (str):      작성자 이름 (예: "Alice")
        timestamp (float): 커밋 생성 시각 (Unix timestamp, time.time() 값)
        parents (List[str]): 부모 커밋의 해시 리스트
    """

    def __init__(self, message: str, author: str, timestamp: float, parents: Optional[List[str]] = None) -> None:
        """
        Commit 객체를 생성합니다.
        """
        # ── 부모 커밋 리스트 초기화 ──
        if parents is not None:
            self.parents: List[str] = parents
        else:
            self.parents: List[str] = []

        self.message: str = message
        self.author: str = author
        self.timestamp: float = timestamp
        self.hash: str = self._generate_hash()

    def _generate_hash(self) -> str:
        """
        SHA-1 해시를 생성하여 앞 6자리 hex 문자열을 반환합니다.
        """
        parent_str: str = ",".join(self.parents)
        content: str = f"{self.message}|{self.author}|{self.timestamp}|{parent_str}"
        return hashlib.sha1(content.encode('utf-8')).hexdigest()[:6]

    def __repr__(self) -> str:
        """
        Commit 객체의 문자열 표현을 반환합니다.
        """
        return f"Commit(hash={self.hash}, message='{self.message}')"


class Repository:
    """
    Mini Git 저장소 전체 상태를 관리하는 클래스.

    Attributes:
        commits (Dict[str, Commit]):      해시 → Commit 객체 매핑 (해시맵)
        branches (Dict[str, Optional[str]]): 브랜치명 → 커밋 해시 매핑
        head (Optional[str]):             현재 활성 브랜치명
        current_user (Optional[str]):     현재 사용자명
        inverted_index (InvertedIndex):   역색인 객체
        initialized (bool):               저장소 초기화 여부
        _hash_set (Set[str]):             생성된 해시 목록 (충돌 방지용)
        _hash_counter (int):              해시 충돌 시 사용하는 카운터
    """

    def __init__(self) -> None:
        """
        Repository 객체를 생성합니다.
        """
        self.commits: Dict[str, Commit] = {}
        self.branches: Dict[str, Optional[str]] = {}
        self.head: Optional[str] = None
        self.current_user: Optional[str] = None
        self.inverted_index: InvertedIndex = InvertedIndex()
        self.initialized: bool = False
        self._hash_set: Set[str] = set()
        self._hash_counter: int = 0

    def _ensure_unique_hash(self, commit: Commit) -> None:
        """
        커밋 해시의 유일성을 보장합니다.
        """
        while commit.hash in self._hash_set:
            self._hash_counter += 1
            content: str = f"{commit.message}|{commit.author}|{commit.timestamp}|{self._hash_counter}"
            commit.hash = hashlib.sha1(content.encode('utf-8')).hexdigest()[:6]
        self._hash_set.add(commit.hash)

    def init(self, user_name: str) -> str:
        """
        저장소를 초기화합니다.
        """
        # ── 1. Data Refinement (데이터 정제) ──
        clean_user_name: str = user_name.strip()
        
        # ── 2. Validation (유효성 검사) ──
        if not clean_user_name:
            return ErrorMessages.INVALID_INIT

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        self.commits = {}
        self.branches = {}
        self._hash_set = set()
        self._hash_counter = 0
        self.inverted_index = InvertedIndex()

        self.branches[ConfigConstants.DEFAULT_BRANCH] = None
        self.head = ConfigConstants.DEFAULT_BRANCH
        self.current_user = clean_user_name
        self.initialized = True

        return SystemMessages.INIT_SUCCESS.format(branch=self.head, user=clean_user_name)

    def commit(self, message: str) -> str:
        """
        새 커밋을 생성합니다.
        """
        # ── 1. Data Refinement (데이터 정제) ──
        clean_message: str = message.strip()

        # ── 2. Validation (유효성 검사) ──
        if not self.initialized:
            return ErrorMessages.REPO_NOT_INIT
        if not clean_message:
            return ErrorMessages.INVALID_COMMIT
            
        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        current_commit_hash: Optional[str] = None
        if self.head is not None:
            current_commit_hash = self.branches.get(self.head)
            
        parents: List[str] = []
        if current_commit_hash is not None:
            parents.append(current_commit_hash)
            
        timestamp: float = time.time()
        new_commit: Commit = Commit(
            message=clean_message,
            author=self.current_user if self.current_user is not None else "Unknown",
            timestamp=timestamp,
            parents=parents
        )
        
        self._ensure_unique_hash(new_commit)
        self.commits[new_commit.hash] = new_commit
        
        if self.head is not None:
            self.branches[self.head] = new_commit.hash
            
        self.inverted_index.add_commit(new_commit)

        return SystemMessages.COMMIT_SUCCESS.format(branch=self.head, hash=new_commit.hash, message=clean_message)

    def branch(self, branch_name: str) -> str:
        """
        새 브랜치를 생성합니다.
        """
        # ── 1. Data Refinement (데이터 정제) ──
        clean_branch_name: str = branch_name.strip()

        # ── 2. Validation (유효성 검사) ──
        if not self.initialized:
            return ErrorMessages.REPO_NOT_INIT
        if not clean_branch_name:
            return ErrorMessages.INVALID_BRANCH
        if clean_branch_name in self.branches:
            return ErrorMessages.BRANCH_ALREADY_EXISTS.format(name=clean_branch_name)

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        if self.head is not None:
            self.branches[clean_branch_name] = self.branches[self.head]
        else:
            self.branches[clean_branch_name] = None
            
        return SystemMessages.BRANCH_CREATED.format(name=clean_branch_name)

    def switch(self, branch_name: str) -> str:
        """
        다른 브랜치로 전환합니다.
        """
        # ── 1. Data Refinement (데이터 정제) ──
        clean_branch_name: str = branch_name.strip()

        # ── 2. Validation (유효성 검사) ──
        if not self.initialized:
            return ErrorMessages.REPO_NOT_INIT
        if not clean_branch_name:
            return ErrorMessages.INVALID_SWITCH
        if clean_branch_name not in self.branches:
            return ErrorMessages.UNKNOWN_BRANCH.format(name=clean_branch_name)

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        self.head = clean_branch_name
        return SystemMessages.SWITCHED_BRANCH.format(name=clean_branch_name)

    def merge(self, branch_name: str) -> str:
        """
        지정된 브랜치를 현재 브랜치로 머지합니다.
        """
        # ── 1. Data Refinement (데이터 정제) ──
        clean_branch_name: str = branch_name.strip()

        # ── 2. Validation (유효성 검사) ──
        if not self.initialized:
            return ErrorMessages.REPO_NOT_INIT
        if not clean_branch_name:
            return ErrorMessages.INVALID_MERGE
        if clean_branch_name not in self.branches:
            return ErrorMessages.UNKNOWN_BRANCH.format(name=clean_branch_name)
        if clean_branch_name == self.head:
            return ErrorMessages.MERGE_SELF

        current_hash: Optional[str] = None
        if self.head is not None:
            current_hash = self.branches.get(self.head)
            
        target_hash: Optional[str] = self.branches.get(clean_branch_name)

        if current_hash is None:
            return ErrorMessages.MERGE_NO_COMMITS
        elif target_hash is None:
            return ErrorMessages.MERGE_NO_COMMITS
            
        if current_hash == target_hash:
            return SystemMessages.ALREADY_UP_TO_DATE

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        merge_message: str = f"Merge branch '{clean_branch_name}' into {self.head}"
        timestamp: float = time.time()
        
        parents: List[str] = [current_hash, target_hash]
        
        merge_commit: Commit = Commit(
            message=merge_message,
            author=self.current_user if self.current_user is not None else "Unknown",
            timestamp=timestamp,
            parents=parents
        )

        self._ensure_unique_hash(merge_commit)
        self.commits[merge_commit.hash] = merge_commit
        
        if self.head is not None:
            self.branches[self.head] = merge_commit.hash
            
        self.inverted_index.add_commit(merge_commit)

        return SystemMessages.MERGE_SUCCESS.format(
            branch=clean_branch_name, 
            head=self.head, 
            hash=merge_commit.hash, 
            message=merge_message
        )

    def get_head_commit_hash(self) -> Optional[str]:
        """
        현재 HEAD가 가리키는 커밋의 해시를 반환합니다.
        """
        if not self.initialized:
            return None
        if self.head is None:
            return None
        return self.branches.get(self.head)

    def get_all_commits(self) -> Dict[str, Commit]:
        """
        저장소의 모든 커밋을 딕셔너리로 반환합니다.
        """
        return self.commits

    def get_commit(self, commit_hash: str) -> Optional[Commit]:
        """
        해시로 특정 커밋을 조회합니다.
        """
        return self.commits.get(commit_hash)
