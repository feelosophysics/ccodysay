"""
diff.py — LCS 기반 Diff(파일 비교) 모듈
=========================================

[보너스 과제 5.1]

이 모듈은 두 텍스트 파일을 줄 단위로 비교하여
추가(+), 삭제(-), 공통( ) 줄을 구분해 출력합니다.
"""

from typing import List, Tuple
from minigit.constants import ErrorMessages


def compute_lcs_table(lines_a: List[str], lines_b: List[str]) -> List[List[int]]:
    """
    두 줄 목록의 LCS DP 테이블을 생성합니다.
    """
    # ── 1. Data Refinement (데이터 정제) ──
    # 파라미터가 이미 정제되어 전달된다고 가정합니다.

    # ── 2. Validation (유효성 검사) ──
    m: int = len(lines_a)
    n: int = len(lines_b)
    
    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    dp: List[List[int]] = []
    for i in range(m + 1):
        row: List[int] = []
        for j in range(n + 1):
            row.append(0)
        dp.append(row)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if lines_a[i - 1] == lines_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                if dp[i - 1][j] >= dp[i][j - 1]:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = dp[i][j - 1]

    return dp


def compute_diff(lines_a: List[str], lines_b: List[str]) -> List[Tuple[str, str]]:
    """
    LCS 테이블을 역추적하여 diff 결과를 생성합니다.
    """
    # ── 1. Data Refinement (데이터 정제) ──
    # 패스

    # ── 2. Validation (유효성 검사) ──
    # 패스

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    dp: List[List[int]] = compute_lcs_table(lines_a, lines_b)

    diff_result: List[Tuple[str, str]] = []
    i: int = len(lines_a)
    j: int = len(lines_b)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and lines_a[i - 1] == lines_b[j - 1]:
            diff_result.append((" ", lines_a[i - 1]))
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or dp[i - 1][j] >= dp[i][j - 1]):
            diff_result.append(("-", lines_a[i - 1]))
            i -= 1
        else:
            diff_result.append(("+", lines_b[j - 1]))
            j -= 1

    diff_result.reverse()
    return diff_result


def diff_files(file1_path: str, file2_path: str) -> str:
    """
    두 텍스트 파일을 비교하여 diff 결과를 문자열로 반환합니다.
    """
    # ── 1. Data Refinement (데이터 정제) ──
    clean_path1: str = file1_path.strip()
    clean_path2: str = file2_path.strip()

    # ── 2. Validation (유효성 검사) ──
    lines_a: List[str] = []
    lines_b: List[str] = []
    
    try:
        with open(clean_path1, 'r', encoding='utf-8') as f:
            lines_a = f.read().splitlines()
    except FileNotFoundError:
        return ErrorMessages.FILE_NOT_FOUND.format(path=clean_path1)
    except OSError as e:
        return ErrorMessages.FILE_READ_ERROR.format(path=clean_path1, error=str(e))

    try:
        with open(clean_path2, 'r', encoding='utf-8') as f:
            lines_b = f.read().splitlines()
    except FileNotFoundError:
        return ErrorMessages.FILE_NOT_FOUND.format(path=clean_path2)
    except OSError as e:
        return ErrorMessages.FILE_READ_ERROR.format(path=clean_path2, error=str(e))

    # ── 3. Logic Execution (비즈니스 로직 실행) ──
    diff_result: List[Tuple[str, str]] = compute_diff(lines_a, lines_b)

    output_lines: List[str] = []
    output_lines.append(f"--- {clean_path1}")
    output_lines.append(f"+++ {clean_path2}")
    output_lines.append("")

    added: int = 0
    removed: int = 0
    unchanged: int = 0

    for mark, line in diff_result:
        if mark == "+":
            output_lines.append(f"+ {line}")
            added += 1
        elif mark == "-":
            output_lines.append(f"- {line}")
            removed += 1
        else:
            output_lines.append(f"  {line}")
            unchanged += 1

    output_lines.append("")
    output_lines.append(
        f"Summary: {added} addition(s), "
        f"{removed} deletion(s), "
        f"{unchanged} unchanged line(s)"
    )

    return "\n".join(output_lines)
