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

    def __post_init__(self) -> None:
        """
         후 유효성 검증

            1. 상위 계정과목 코드가 없을 경우 현재 계정과목 코드에 언더바(_)가 없는지 검사
            2. 현재 계정과목 코드가 상위 계정과목 코드로 시작하는지 검사

        Raises:
            ValueError: 상위 계정과목 코드가 없을 경우 발생
            ValueError: 현재 계정과목 코드가 상위 계정과목 코드로 시작하지 않을 경우 발생
        """
        if self.parent_code is None and "_" in self.code:
            raise ValueError(f"code must not contain '_' if parent_code is None. (Currently: {self.code})")

        if self.parent_code and self.code.rpartition("_")[0] != self.parent_code:
            raise ValueError(
                f"Parent chart of account with code {self.parent_code} must be a prefix of the current account's code {self.code}."
            )


@dataclass(frozen=True)
class UpdateChartOfAccountCommand:
    """
    계정과목 수정 명령

    변경할 수 있는 속성만 유지

    Args:
        name: 계정과목 이름
        is_hidden: 계정과목 숨김 여부
        description: 계정과목 설명
    """

    name: str
    is_hidden: bool
    description: str
