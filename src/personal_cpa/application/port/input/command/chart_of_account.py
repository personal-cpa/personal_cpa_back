from dataclasses import dataclass

from personal_cpa.domain.enum.chart_of_account import AccountType


@dataclass(frozen=True)
class CreateChartOfAccountCommand:
    """
    계정과목 생성 명령

    Args:
        code: 계정과목 코드
        name: 계정과목 이름
        category: 계정과목 카테고리
        description: 계정과목 설명
        parent_code: 상위 계정과목 코드
    """

    code: str
    name: str
    category: AccountType
    description: str | None
    parent_code: str | None


@dataclass(frozen=True)
class UpdateChartOfAccountCommand:
    """
    계정과목 수정 명령

    Args:
        name: 계정과목 이름
        category: 계정과목 카테고리
        is_hidden: 계정과목 숨김 여부
        description: 계정과목 설명
    """

    name: str
    category: AccountType
    is_hidden: bool
    description: str | None
