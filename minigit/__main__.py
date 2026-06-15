"""
__main__.py — Mini Git CLI 진입점 (REPL)
======================================

패키지로 실행할 때의 진입점입니다. (python -m minigit)
REPL(Read-Eval-Print Loop) 패턴으로 동작하며, 
모든 라우팅과 상태 관리를 MiniGitCLI 클래스에 캡슐화합니다.
"""

import shlex
import datetime
from typing import List, Optional, Dict, Set

from minigit.models import Repository, Commit
from minigit.graph import topological_sort, find_shortest_path, find_ancestors
from minigit.sorting import merge_sort, benchmark_sorts
from minigit.diff import diff_files
from minigit.constants import CommandType, SystemMessages, ErrorMessages, ConfigConstants


def format_timestamp(ts: float) -> str:
    """
    Unix 타임스탬프를 사람이 읽을 수 있는 형식으로 변환합니다.
    """
    dt: datetime.datetime = datetime.datetime.fromtimestamp(ts)
    return dt.strftime(ConfigConstants.TIME_FORMAT)


class MiniGitCLI:
    """
    Mini Git CLI의 상태와 명령어 라우팅을 캡슐화하는 클래스.
    """
    def __init__(self) -> None:
        """
        CLI 초기화 시 빈 저장소를 생성합니다.
        """
        self.repo: Repository = Repository()

    def parse_input(self, user_input: str) -> List[str]:
        """
        사용자 입력을 명령어와 인자로 분리합니다.
        """
        # ── 1. Data Refinement (데이터 정제) ──
        clean_input: str = user_input.strip()

        # ── 2. Validation (유효성 검사) ──
        if not clean_input:
            return []

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        tokens: List[str] = []
        try:
            tokens = shlex.split(clean_input)
        except ValueError:
            tokens = clean_input.split()

        return tokens

    def handle_init(self, args: List[str]) -> str:
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스 (Repository 내부에서 처리)
        
        # ── 2. Validation (유효성 검사) ──
        if len(args) < 1:
            return ErrorMessages.INVALID_INIT
            
        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        user_name: str = args[0]
        return self.repo.init(user_name)

    def handle_commit(self, args: List[str]) -> str:
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스

        # ── 2. Validation (유효성 검사) ──
        if len(args) < 1:
            return ErrorMessages.INVALID_COMMIT
            
        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        message: str = " ".join(args)
        return self.repo.commit(message)

    def handle_branch(self, args: List[str]) -> str:
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스

        # ── 2. Validation (유효성 검사) ──
        if len(args) < 1:
            return ErrorMessages.INVALID_BRANCH
            
        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        return self.repo.branch(args[0])

    def handle_switch(self, args: List[str]) -> str:
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스

        # ── 2. Validation (유효성 검사) ──
        if len(args) < 1:
            return ErrorMessages.INVALID_SWITCH
            
        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        return self.repo.switch(args[0])

    def handle_log(self, args: List[str]) -> str:
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스

        # ── 2. Validation (유효성 검사) ──
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        commits_dict: Dict[str, Commit] = self.repo.get_all_commits()
        if not commits_dict:
            return SystemMessages.NO_COMMITS_YET

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        sort_by: Optional[str] = None
        for arg in args:
            if arg.startswith("--sort-by="):
                sort_by = arg.split("=", 1)[1].lower()

        sorted_commits: List[Commit] = []
        
        if sort_by is not None:
            commits_list: List[Commit] = list(commits_dict.values())
            if sort_by == "date":
                sorted_commits = merge_sort(commits_list, key_func=lambda c: c.timestamp)
            elif sort_by == "author":
                sorted_commits = merge_sort(commits_list, key_func=lambda c: c.author.lower())
            else:
                return ErrorMessages.INVALID_SORT_KEY.format(key=sort_by)
        else:
            sorted_commits = topological_sort(commits_dict)

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
            if self.repo.head is not None and self.repo.branches.get(self.repo.head) == commit.hash:
                head_marker = " (HEAD)"

            lines.append(f"commit {commit.hash} ({commit.author}, {time_str}){branch_str}{head_marker}")
            lines.append(f"  {commit.message}")
            lines.append("")

        return "\n".join(lines).rstrip()

    def handle_path(self, args: List[str]) -> str:
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스

        # ── 2. Validation (유효성 검사) ──
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

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
        path: Optional[List[str]] = find_shortest_path(self.repo.commits, hash1, hash2)

        if path is None:
            return SystemMessages.NO_PATH

        path_str: str = " -> ".join(path)
        return f"Path: {path_str}"

    def handle_ancestors(self, args: List[str]) -> str:
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스

        # ── 2. Validation (유효성 검사) ──
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        if len(args) < 1:
            return ErrorMessages.INVALID_ANCESTORS

        commit_hash: str = args[0]

        if commit_hash not in self.repo.commits:
            return ErrorMessages.UNKNOWN_COMMIT.format(hash=commit_hash)

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
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
        # ── 1. Data Refinement (데이터 정제) ──
        # 패스

        # ── 2. Validation (유효성 검사) ──
        if not self.repo.initialized:
            return ErrorMessages.REPO_NOT_INIT

        if len(args) < 1:
            return ErrorMessages.INVALID_SEARCH

        # ── 3. Logic Execution (비즈니스 로직 실행) ──
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

    def run(self) -> None:
        """
        CLI 메인 실행 루프
        """
        print(SystemMessages.WELCOME)
        print()

        while True:
            try:
                user_input: str = input(SystemMessages.PROMPT)
            except EOFError:
                print(SystemMessages.GOODBYE)
                break
            except KeyboardInterrupt:
                print()
                continue

            tokens: List[str] = self.parse_input(user_input)
            if not tokens:
                continue

            command_str: str = tokens[0].upper()
            args: List[str] = tokens[1:]
            result: str = ""

            # ── 명시적 분기 처리 ──
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


if __name__ == "__main__":
    cli: MiniGitCLI = MiniGitCLI()
    cli.run()
