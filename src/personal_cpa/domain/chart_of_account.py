from __future__ import annotations

from dataclasses import dataclass

from personal_cpa.domain.enum.chart_of_account import AccountType


@dataclass
class ChartOfAccount:
    """
    사용자의 계정과목을 표현하는 도메인 모델.

    복식부기 시스템에서 자산/부채/자본/수익/비용 등의 유형을 가진 계정을 나타내며,
    계정명, 코드, 상위 계정 정보 등을 포함한다.
    """

    user_id: int
    code: str
    name: str
    category: AccountType
    description: str | None
    parent_chart_of_account_id: int | None
    is_hidden: bool = False
    id: int | None = None

    _VALID_CODE_CHARACTER = "01234567890_"

    def __post_init__(self):
        """
        생성 후 필드 유효성 검사를 수행합니다.

        - name과 code는 공백이 아닌 값을 가져야 합니다.
        - code는 숫자와 언더바(_)만 허용합니다.
        - code는 언더바(_)로 끝나면 안 됩니다.
        - category은 AccountType Enum이어야 합니다.

        Raises:
            ValueError: name, code가 비어 있거나 code가 허용되지 않은 문자를 포함할 경우,
                        혹은 상위 계정과 category이 일치하지 않을 경우 발생합니다.
            TypeError: type이 AccountType이 아닌 경우 발생합니다.
        """
        if not self.name.strip():
            raise ValueError("name is not empty.")
        if not self.code.strip():
            raise ValueError("code is not empty.")
        if any(c not in self._VALID_CODE_CHARACTER for c in self.code):
            raise ValueError(f"code can only be a number OR '_'. (Currently: {self.code})")
        if self.code.endswith("_"):
            raise ValueError(f"code must not end with '_'. (Currently: {self.code})")
        if not isinstance(self.category, AccountType):
            raise TypeError(f"type must be an AccountType enum. (Currently: {type(self.category)})")


@dataclass
class ChartOfAccountTree:
    """
    계정과목 트리를 표현하는 도메인 모델.
    """

    user_id: int
    code: str
    name: str
    category: AccountType
    children: list[ChartOfAccountTree]
    description: str | None
    parent_chart_of_account_id: int | None
    id: int | None = None
