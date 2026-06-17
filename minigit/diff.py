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
    # 💡 파이썬 현미경 해설
    # DP(Dynamic Programming, 동적 계획법)를 위한 2차원 표(리스트 안의 리스트)를 만듭니다.
    dp: List[List[int]] = []
    
    # `range(m + 1)`: 0부터 m까지 반복합니다.
    for i in range(m + 1):
        row: List[int] = []
        for j in range(n + 1):
            row.append(0)  # 표를 처음엔 전부 0으로 채웁니다.
        dp.append(row)

    # 💡 파이썬 현미경 해설
    # LCS(최장 공통 부분 수열) 알고리즘의 핵심 로직입니다.
    # 두 글자(여기서는 '줄')가 같으면 이전 대각선 값 + 1 을 하고,
    # 다르면 위쪽이나 왼쪽 중 더 큰 값을 끌어옵니다.
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


# 💡 파이썬 현미경 해설
# `Tuple`은 리스트와 비슷하지만 한 번 만들어지면 수정이 불가능한 '소포(꾸러미)'입니다.
# `Tuple[str, str]`은 문자열 두 개가 세트로 묶여있다는 뜻입니다. 예: ("+", "hello")
def compute_diff(lines_a: List[str], lines_b: List[str]) -> List[Tuple[str, str]]:
    """
    LCS 테이블을 역추적하여 diff 결과를 생성합니다.
    """
    dp: List[List[int]] = compute_lcs_table(lines_a, lines_b)

    diff_result: List[Tuple[str, str]] = []
    i: int = len(lines_a)
    j: int = len(lines_b)

    # 💡 파이썬 현미경 해설
    # 테이블의 맨 오른쪽 아래에서 출발해 위나 왼쪽으로 역추적해 올라갑니다.
    while i > 0 or j > 0:
        # 두 줄이 같았다면: 대각선 위로 올라가며 '공통 부분( )'으로 기록
        if i > 0 and j > 0 and lines_a[i - 1] == lines_b[j - 1]:
            # 괄호로 묶인 `(" ", lines_a[i - 1])`이 바로 튜플(Tuple)입니다!
            diff_result.append((" ", lines_a[i - 1]))
            i -= 1
            j -= 1
        # 위쪽 값이 더 컸거나 왼쪽 끝에 다다랐다면: 위로 올라가며 '삭제됨(-)'으로 기록
        elif i > 0 and (j == 0 or dp[i - 1][j] >= dp[i][j - 1]):
            diff_result.append(("-", lines_a[i - 1]))
            i -= 1
        # 왼쪽 값이 더 컸거나 위쪽 끝에 다다랐다면: 왼쪽으로 가며 '추가됨(+)'으로 기록
        else:
            diff_result.append(("+", lines_b[j - 1]))
            j -= 1

    # 거꾸로 올라갔으니 결과를 다시 뒤집어줍니다.
    diff_result.reverse()
    return diff_result


def diff_files(file1_path: str, file2_path: str) -> str:
    """
    두 텍스트 파일을 비교하여 diff 결과를 문자열로 반환합니다.
    """
    clean_path1: str = file1_path.strip()
    clean_path2: str = file2_path.strip()

    lines_a: List[str] = []
    lines_b: List[str] = []
    
    # 💡 파이썬 현미경 해설
    # `try ... except ...` : 에러가 날 수도 있는 불안한 코드(파일 읽기)를 실행할 때,
    # 프로그램이 뻗어버리지 않게 안전망을 쳐두는 문법입니다.
    try:
        # `with open(...) as f:` : 파일을 열고 나서 `with` 블록이 끝나면 파이썬이 "알아서" 파일을 안전하게 닫아줍니다.
        with open(clean_path1, 'r', encoding='utf-8') as f:
            # `.read().splitlines()` : 파일 전체를 읽은 다음, 엔터 단위로 쪼개서 리스트로 만들어줍니다.
            lines_a = f.read().splitlines()
    except FileNotFoundError:
        # 파일을 찾지 못했을 때 실행됩니다.
        return ErrorMessages.FILE_NOT_FOUND.format(path=clean_path1)
    except OSError as e:
        # 파일은 찾았는데 읽기 권한이 없거나 다른 에러가 났을 때 실행됩니다.
        # `str(e)`로 에러의 상세 원인을 텍스트로 뽑아옵니다.
        return ErrorMessages.FILE_READ_ERROR.format(path=clean_path1, error=str(e))

    try:
        with open(clean_path2, 'r', encoding='utf-8') as f:
            lines_b = f.read().splitlines()
    except FileNotFoundError:
        return ErrorMessages.FILE_NOT_FOUND.format(path=clean_path2)
    except OSError as e:
        return ErrorMessages.FILE_READ_ERROR.format(path=clean_path2, error=str(e))

    # 두 파일을 다 잘 읽어왔다면 위에서 만든 diff 계산 함수를 부릅니다.
    diff_result: List[Tuple[str, str]] = compute_diff(lines_a, lines_b)

    output_lines: List[str] = []
    # 전통적인 diff 도구들처럼 이전 파일은 ---, 바뀐 파일은 +++로 표시합니다.
    output_lines.append(f"--- {clean_path1}")
    output_lines.append(f"+++ {clean_path2}")
    output_lines.append("")

    added: int = 0
    removed: int = 0
    unchanged: int = 0

    # 💡 파이썬 현미경 해설
    # `for mark, line in diff_result:`
    # 튜플 묶음 `("+", "hello")`을 한 번에 풀어헤쳐서 앞부분은 mark에, 뒷부분은 line에 집어넣는 아주 세련된 파이썬 문법(Unpacking)입니다!
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
