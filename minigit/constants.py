"""
constants.py — Mini Git 상수 및 메시지 모음
============================================

이 모듈은 Mini Git 전반에서 사용되는 모든 상수, 매직 스트링,
에러 메시지 등을 중앙 집중식으로 관리합니다.
"""

from enum import Enum


class CommandType(Enum):
    """CLI 명령어의 종류를 정의하는 Enum 클래스"""
    INIT = "INIT"
    COMMIT = "COMMIT"
    BRANCH = "BRANCH"
    SWITCH = "SWITCH"
    LOG = "LOG"
    PATH = "PATH"
    ANCESTORS = "ANCESTORS"
    SEARCH = "SEARCH"
    MERGE = "MERGE"
    DIFF = "DIFF"
    BENCHMARK = "BENCHMARK"
    STATUS = "STATUS"
    HELP = "HELP"
    EXIT = "EXIT"
    QUIT = "QUIT"


class ConfigConstants:
    """시스템 기본 설정값들을 관리하는 클래스"""
    DEFAULT_BRANCH = "main"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class ErrorMessages:
    """모든 에러 메시지를 관리하는 텍스트 클래스"""
    REPO_NOT_INIT = "Error: Repository not initialized. Use INIT first."
    BRANCH_ALREADY_EXISTS = "Error: Branch '{name}' already exists."
    UNKNOWN_BRANCH = "Error: Unknown branch: {name}"
    UNKNOWN_COMMIT = "Error: Unknown commit: {hash}"
    MERGE_SELF = "Error: Cannot merge a branch into itself."
    MERGE_NO_COMMITS = "Error: Cannot merge branches without commits."
    INVALID_INIT = "Error: Invalid args: INIT <user_name>"
    INVALID_COMMIT = "Error: Invalid args: COMMIT <message>"
    INVALID_BRANCH = "Error: Invalid args: BRANCH <branch_name>"
    INVALID_SWITCH = "Error: Invalid args: SWITCH <branch_name>"
    INVALID_PATH = "Error: Invalid args: PATH <commit1> <commit2>"
    INVALID_ANCESTORS = "Error: Invalid args: ANCESTORS <commit_hash>"
    INVALID_SEARCH = "Error: Invalid args: SEARCH <keyword> or SEARCH --author=<name>"
    INVALID_MERGE = "Error: Invalid args: MERGE <branch_name>"
    INVALID_DIFF = "Error: Invalid args: DIFF <file1> <file2>"
    INVALID_SORT_KEY = "Error: Invalid sort key: {key}. Use 'date' or 'author'."
    FILE_NOT_FOUND = "Error: File not found: {path}"
    FILE_READ_ERROR = "Error: Error reading {path}: {error}"


class SystemMessages:
    """일반 출력 및 상태 메시지를 관리하는 텍스트 클래스"""
    PROMPT = "mini-git> "
    WELCOME = (
        "==================================================\n"
        "  Welcome to Mini Git!\n"
        "  Type 'help' for available commands.\n"
        "=================================================="
    )
    GOODBYE = "Goodbye!"
    UNKNOWN_COMMAND = "Unknown command: {command}. Type 'help' for available commands."
    ALREADY_UP_TO_DATE = "Already up to date."
    NO_COMMITS_YET = "No commits yet."
    NO_PATH = "No path"

    INIT_SUCCESS = "Initialized repository.\nCurrent branch: {branch}\nCurrent user: {user}"
    COMMIT_SUCCESS = "[{branch} {hash}] {message}"
    BRANCH_CREATED = "Created branch: {name}"
    SWITCHED_BRANCH = "Switched to branch: {name}"
    MERGE_SUCCESS = "Merged '{branch}' into '{head}'.\n[{head} {hash}] {message}"
    
    SEARCH_NO_RESULTS = "No commits found for {search_type}."
    SEARCH_FOUND = "Found {count} commit(s) for {search_type}:"
    
    HELP_TEXT = """
╔══════════════════════════════════════════════════════════════╗
║                    Mini Git — Command Help                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  INIT <user_name>         Initialize repository              ║
║  COMMIT <message>         Create a new commit                ║
║  BRANCH <name>            Create a new branch                ║
║  SWITCH <name>            Switch to a branch                 ║
║  LOG                      Show commits (topological order)   ║
║  LOG --sort-by=date       Show commits sorted by date        ║
║  LOG --sort-by=author     Show commits sorted by author      ║
║  PATH <hash1> <hash2>     Find shortest path between commits ║
║  ANCESTORS <hash>         Find all ancestors of a commit     ║
║  SEARCH <keyword>         Search commits by keyword          ║
║  SEARCH --author=<name>   Search commits by author           ║
║  STATUS                   Show repository status             ║
║                                                              ║
║  ── Bonus Commands ──                                        ║
║  MERGE <branch_name>      Merge a branch into current        ║
║  DIFF <file1> <file2>     Compare two text files (LCS)       ║
║  BENCHMARK                Compare sorting algorithms         ║
║                                                              ║
║  HELP                     Show this help message             ║
║  EXIT / QUIT              Exit Mini Git                      ║
╚══════════════════════════════════════════════════════════════╝
"""

    BENCHMARK_HEADER = (
        "=================================================================\n"
        "  Sorting Algorithm Benchmark: Merge Sort vs Quick Sort\n"
        "=================================================================\n"
        f"{'Size':>8} | {'Merge Sort (s)':>16} | {'Quick Sort (s)':>16} | {'Winner':>8}\n"
        "-----------------------------------------------------------------"
    )
    BENCHMARK_ROW = "{size:>8} | {merge:>16.6f} | {quick:>16.6f} | {winner:>8}"
    BENCHMARK_FOOTER = (
        "-----------------------------------------------------------------\n\n"
        "Notes:\n"
        "  - Merge Sort: Stable, O(n log n) guaranteed\n"
        "  - Quick Sort: Unstable, O(n log n) avg, O(n^2) worst\n"
        "  - Merge Sort uses O(n) extra space\n"
        "  - Quick Sort (this impl) also uses O(n) extra space\n"
        "    (due to list creation; in-place version uses O(log n))\n"
        "================================================================="
    )
