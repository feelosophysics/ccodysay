"""
__main__.py — Mini Git CLI 진입점 (REPL)
======================================

패키지로 실행할 때의 진입점입니다. (python -m minigit)
REPL(Read-Eval-Print Loop) 패턴으로 동작하며, 
모든 라우팅과 상태 관리를 MiniGitCLI 클래스에 캡슐화합니다.

# 💡 파이썬 현미경 해설
# `__main__.py`는 파이썬에서 특별한 이름입니다.
# 어떤 폴더(여기서는 minigit)를 통째로 프로그램처럼 실행하라고 명령했을 때
# 파이썬이 가장 먼저 찾아서 실행하는 '메인 대문' 역할을 합니다!
"""

# 💡 파이썬 현미경 해설
# `import ...` 는 다른 사람이 만들어 둔 유용한 도구나
# 우리가 다른 파일에 만들어둔 코드들을 가져와서 쓰겠다는 뜻입니다.
import shlex
import datetime
from typing import List, Optional, Dict, Set

# `from 폴더.파일 import 이름` 형태입니다.
from minigit.models import Repository, Commit
from minigit.graph import topological_sort, find_shortest_path, find_ancestors
from minigit.sorting import merge_sort, benchmark_sorts
from minigit.diff import diff_files
from minigit.constants import CommandType, SystemMessages, ErrorMessages, ConfigConstants


# 💡 파이썬 현미경 해설
# `def`로 함수를 정의합니다.
# `ts: float`는 'ts'라는 이름의 변수가 들어오는데, 그건 소수점이 있는 숫자(float)라는 뜻입니다.
def format_timestamp(ts: float) -> str:
    """
    Unix 타임스탬프를 사람이 읽을 수 있는 형식으로 변환합니다.
    """
    # 💡 파이썬 현미경 해설
    # 컴퓨터는 시간을 "1970년 1월 1일부터 몇 초가 지났나?"(Unix Timestamp)로 기억합니다.
    # 그걸 우리가 읽을 수 있는 날짜 객체로 바꾼 다음,
    dt: datetime.datetime = datetime.datetime.fromtimestamp(ts)
    # `.strftime`을 써서 년-월-일 시:분:초 형태로 예쁘게 화장시켜 돌려줍니다!
    return dt.strftime(ConfigConstants.TIME_FORMAT)


class MiniGitCLI:
    """
    Mini Git CLI의 상태와 명령어 라우팅을 캡슐화하는 클래스.
    """
    # 💡 파이썬 현미경 해설
    # 이 프로그램이 처음 켜질 때 한 번 실행되는 초기화 설정 버튼입니다.
    def __init__(self) -> None:
        """
        CLI 초기화 시 빈 저장소를 생성합니다.
        """
        # 내 주머니(`self.repo`)에 텅 빈 저장소 붕어빵(`Repository()`)을 하나 구워 넣습니다.
        self.repo: Repository = Repository()

    def parse_input(self, user_input: str) -> List[str]:
        """
        사용자 입력을 명령어와 인자로 분리합니다.
        """
        # ── 1. Data Refinement (데이터 정제) ──
        # 사용자가 엔터를 잘못 치거나 양옆에 띄어쓰기를 넣었을 수 있으니 깔끔하게 잘라줍니다.
        clean_input: str = user_input.strip()

        # ── 2. Validation (유효성 검사) ──
        # 아무것도 안 치고 엔터만 쳤다면 빈 리스트를 돌려줍니다.
        if not clean_input:
            return []

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        tokens: List[str] = []
        # 💡 파이썬 현미경 해설
        # `try ... except ...`: 불안한 코드 안전망!
        try:
            # `shlex.split()`은 사용자가 따옴표(" ")로 묶어서 친 문장은 하나의 단어로 똑똑하게 쪼개주는 도구입니다.
            # 예: commit "hello world" -> ["commit", "hello world"]
            tokens = shlex.split(clean_input)
        except ValueError:
            # 만약 사용자가 따옴표를 하나만 치는 등 문법을 틀려서 에러가 나면 뻗지 말고,
            # 그냥 단순 무식하게 띄어쓰기 기준으로 쪼개버리라는 뜻입니다!
            tokens = clean_input.split()

        return tokens

    # 💡 파이썬 현미경 해설
    # 아래부터는 사용자가 친 명령어에 따라 각기 다른 함수들이 출동해서 일을 처리합니다.
    # 사용자가 친 단어들의 목록이 `args: List[str]`로 전달됩니다.
    def handle_init(self, args: List[str]) -> str:
        # ── 2. Validation (유효성 검사) ──
        # args 안에 이름이 없으면 에러를 반환합니다.
        if len(args) < 1:
            return ErrorMessages.INVALID_INIT
            
        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        # 첫 번째 단어(인덱스 0번)를 유저 이름으로 삼습니다. 파이썬은 숫자를 0부터 셉니다!
        user_name: str = args[0]
        # 진짜 일을 하는 건 내 주머니 속 `repo`입니다.
        return self.repo.init(user_name)

    def handle_commit(self, args: List[str]) -> str:
        if len(args) < 1:
            return ErrorMessages.INVALID_COMMIT
            
        # 💡 파이썬 현미경 해설
        # `" ".join(args)`는 쪼개져 있던 단어들 사이에 다시 스페이스바(" ")를 넣어서 하나의 문장으로 이어 붙입니다.
        message: str = " ".join(args)
        return self.repo.commit(message)

    def handle_branch(self, args: List[str]) -> str:
        if len(args) < 1:
            return ErrorMessages.INVALID_BRANCH
            
        return self.repo.branch(args[0])

    def handle_switch(self, args: List[str]) -> str:
        if len(args) < 1:
            return ErrorMessages.INVALID_SWITCH
            
        return self.repo.switch(args[0])

    def handle_log(self, args: List[str]) -> str:
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        commits_dict: Dict[str, Commit] = self.repo.get_all_commits()
        if not commits_dict:
            return SystemMessages.NO_COMMITS_YET

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        sort_by: Optional[str] = None
        
        # 💡 파이썬 현미경 해설
        # args(입력한 단어들)를 하나씩 살펴보며 "--sort-by="로 시작하는 단어가 있는지 찾습니다.
        for arg in args:
            if arg.startswith("--sort-by="):
                # `.split("=", 1)`은 "="를 기준으로 딱 한 번만 쪼개라는 뜻입니다.
                # 쪼개면 ["--sort-by", "date"] 처럼 2개가 나오는데, 그 중 1번째(즉 "date" 부분)를 가져옵니다.
                sort_by = arg.split("=", 1)[1].lower()

        sorted_commits: List[Commit] = []
        
        if sort_by is not None:
            # 딕셔너리에 들어있던 커밋 객체들만 싹 모아서 리스트로 바꿉니다.
            commits_list: List[Commit] = list(commits_dict.values())
            
            # 💡 파이썬 현미경 해설
            # `lambda`는 "이름이 없는 초미니 함수"입니다.
            # `lambda c: c.timestamp` = "c가 들어오면 c.timestamp를 내뱉는 함수"라는 뜻입니다!
            if sort_by == "date":
                sorted_commits = merge_sort(commits_list, key_func=lambda c: c.timestamp)
            elif sort_by == "author":
                sorted_commits = merge_sort(commits_list, key_func=lambda c: c.author.lower())
            else:
                return ErrorMessages.INVALID_SORT_KEY.format(key=sort_by)
        else:
            # 아무 옵션이 없으면 기본적으로 우리가 만든 위상 정렬을 수행합니다.
            sorted_commits = topological_sort(commits_dict)

        # 💡 파이썬 현미경 해설
        # 각 커밋이 어떤 브랜치들에 연결되어 있는지 찾기 위해 '해시 -> 브랜치 목록' 딕셔너리를 만듭니다.
        hash_to_branches: Dict[str, List[str]] = {}
        for branch_name, branch_hash in self.repo.branches.items():
            if branch_hash is not None:
                if branch_hash not in hash_to_branches:
                    hash_to_branches[branch_hash] = []
                hash_to_branches[branch_hash].append(branch_name)

        lines: List[str] = []
        for commit in sorted_commits:
            time_str: str = format_timestamp(commit.timestamp)
            
            branch_labels: List[str] = hash_to_branches.get(commit.hash, [])
            branch_str: str = ""
            if branch_labels:
                branch_str = " [" + ", ".join(branch_labels) + "]"

            head_marker: str = ""
            # 현재 머무는 브랜치가 가리키는 곳에 (HEAD) 표시를 붙여줍니다.
            if self.repo.head is not None and self.repo.branches.get(self.repo.head) == commit.hash:
                head_marker = " (HEAD)"

            lines.append(f"commit {commit.hash} ({commit.author}, {time_str}){branch_str}{head_marker}")
            lines.append(f"  {commit.message}")
            lines.append("")

        return "\n".join(lines).rstrip()

    def handle_path(self, args: List[str]) -> str:
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        if len(args) < 2:
            return ErrorMessages.INVALID_PATH

        hash1: str = args[0]
        hash2: str = args[1]

        if hash1 not in self.repo.commits:
            return ErrorMessages.UNKNOWN_COMMIT.format(hash=hash1)
        if hash2 not in self.repo.commits:
            return ErrorMessages.UNKNOWN_COMMIT.format(hash=hash2)

        path: Optional[List[str]] = find_shortest_path(self.repo.commits, hash1, hash2)

        if path is None:
            return SystemMessages.NO_PATH

        path_str: str = " -> ".join(path)
        return f"Path: {path_str}"

    def handle_ancestors(self, args: List[str]) -> str:
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        if len(args) < 1:
            return ErrorMessages.INVALID_ANCESTORS

        commit_hash: str = args[0]

        if commit_hash not in self.repo.commits:
            return ErrorMessages.UNKNOWN_COMMIT.format(hash=commit_hash)

        ancestors: List[str] = find_ancestors(self.repo.commits, commit_hash)

        if not ancestors:
            return f"No ancestors found for commit {commit_hash}"

        lines: List[str] = [f"Ancestors of {commit_hash}:"]
        for ancestor_hash in ancestors:
            commit: Optional[Commit] = self.repo.get_commit(ancestor_hash)
            if commit is not None:
                time_str: str = format_timestamp(commit.timestamp)
                lines.append(f"  {commit.hash} ({commit.author}, {time_str}): {commit.message}")
            else:
                lines.append(f"  {ancestor_hash}")

        return "\n".join(lines)

    def handle_search(self, args: List[str]) -> str:
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        if len(args) < 1:
            return ErrorMessages.INVALID_SEARCH

        search_type: str = ""
        commit_hashes: Set[str] = set()

        if args[0].startswith("--author="):
            author_name: str = args[0].split("=", 1)[1]
            commit_hashes = self.repo.inverted_index.search_author(author_name)
            search_type = f"author '{author_name}'"
        else:
            keyword: str = " ".join(args).lower()
            commit_hashes = self.repo.inverted_index.search_keyword(keyword)
            search_type = f"keyword '{keyword}'"

        if not commit_hashes:
            return SystemMessages.SEARCH_NO_RESULTS.format(search_type=search_type)

        lines: List[str] = [SystemMessages.SEARCH_FOUND.format(count=len(commit_hashes), search_type=search_type), ""]

        for commit_hash in commit_hashes:
            commit: Optional[Commit] = self.repo.get_commit(commit_hash)
            if commit is not None:
                lines.append(f"  - {commit.hash}: {commit.message}")

        return "\n".join(lines)

    def handle_merge(self, args: List[str]) -> str:
        if len(args) < 1:
            return ErrorMessages.INVALID_MERGE
        return self.repo.merge(args[0])

    def handle_diff(self, args: List[str]) -> str:
        if len(args) < 2:
            return ErrorMessages.INVALID_DIFF
        return diff_files(args[0], args[1])

    def handle_benchmark(self) -> str:
        return benchmark_sorts()

    def handle_status(self) -> str:
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        lines: List[str] = []
        lines.append(f"Current user:   {self.repo.current_user}")
        lines.append(f"Current branch: {self.repo.head}")

        head_hash: Optional[str] = self.repo.get_head_commit_hash()
        if head_hash is not None:
            commit: Optional[Commit] = self.repo.get_commit(head_hash)
            if commit is not None:
                lines.append(f"HEAD commit:    {head_hash} - {commit.message}")
        else:
            lines.append("HEAD commit:    (no commits yet)")

        lines.append(f"Total commits:  {len(self.repo.commits)}")
        branches_str: str = ", ".join(self.repo.branches.keys())
        lines.append(f"Branches:       {branches_str}")

        return "\n".join(lines)

    def handle_help(self) -> str:
        return SystemMessages.HELP_TEXT.strip()

    # 💡 파이썬 현미경 해설
    # 터미널에서 계속 입력을 기다리는 "메인 반복 루프"입니다.
    def run(self) -> None:
        """
        CLI 메인 실행 루프
        """
        print(SystemMessages.WELCOME)
        print()

        # `while True:` 무한 반복! 사용자가 끄기 전까지는 프로그램이 종료되지 않습니다.
        while True:
            try:
                # 파이썬의 `input()` 함수는 터미널 화면에 커서를 깜빡이며 사용자의 타이핑을 기다립니다.
                user_input: str = input(SystemMessages.PROMPT)
            except EOFError:
                # (Ctrl+D)를 눌러서 강제로 끊었을 때
                print(SystemMessages.GOODBYE)
                break
            except KeyboardInterrupt:
                # (Ctrl+C)를 눌렀을 때
                print()
                continue

            # 아까 만든 파싱 함수로 입력 문장을 단어 리스트로 쪼갭니다.
            tokens: List[str] = self.parse_input(user_input)
            if not tokens:
                continue

            # 첫 단어가 명령어! 소문자로 쳐도 대문자로 바꿔서(.upper()) 찰떡같이 알아듣습니다.
            command_str: str = tokens[0].upper()
            # 💡 파이썬 현미경 해설
            # `tokens[1:]` : 첫 단어(명령어)를 빼고, 1번째 방부터 끝까지의 모든 단어를 args로 만듭니다. (슬라이싱)
            args: List[str] = tokens[1:]
            result: str = ""

            # ── 명시적 분기 처리 ──
            # if, elif(else if), else를 통해 어떤 명령어인지 찾아가서 맞는 함수를 호출합니다!
            if command_str == CommandType.EXIT.value or command_str == CommandType.QUIT.value:
                print(SystemMessages.GOODBYE)
                break
            elif command_str == CommandType.INIT.value:
                result = self.handle_init(args)
            elif command_str == CommandType.COMMIT.value:
                result = self.handle_commit(args)
            elif command_str == CommandType.BRANCH.value:
                result = self.handle_branch(args)
            elif command_str == CommandType.SWITCH.value:
                result = self.handle_switch(args)
            elif command_str == CommandType.LOG.value:
                result = self.handle_log(args)
            elif command_str == CommandType.PATH.value:
                result = self.handle_path(args)
            elif command_str == CommandType.ANCESTORS.value:
                result = self.handle_ancestors(args)
            elif command_str == CommandType.SEARCH.value:
                result = self.handle_search(args)
            elif command_str == CommandType.MERGE.value:
                result = self.handle_merge(args)
            elif command_str == CommandType.DIFF.value:
                result = self.handle_diff(args)
            elif command_str == CommandType.BENCHMARK.value:
                result = self.handle_benchmark()
            elif command_str == CommandType.STATUS.value:
                result = self.handle_status()
            elif command_str == CommandType.HELP.value:
                result = self.handle_help()
            else:
                result = SystemMessages.UNKNOWN_COMMAND.format(command=tokens[0])

            if result:
                print(result)
                print()

# 💡 파이썬 현미경 해설
# 이 파일이 "다른 곳에서 불려온(import)" 것이 아니라,
# 터미널에서 `python -m minigit`처럼 "직접 대빵으로 실행"되었을 때만 이 아래 코드를 실행하라는 뜻입니다!
if __name__ == "__main__":
    cli: MiniGitCLI = MiniGitCLI()
    cli.run()
