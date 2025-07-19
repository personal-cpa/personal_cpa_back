from abc import ABC, abstractmethod
from typing import Any

from personal_cpa.domain.chart_of_account import ChartOfAccount


class ChartOfAccountPort(ABC):
    """
    계정과목 저장소 인터페이스
    """

    @abstractmethod
    def save_chart_of_accounts(self, chart_of_accounts: list[ChartOfAccount]) -> list[ChartOfAccount]:
        """
        유저의 계정과목 생성 (여러 개)

        Args:
            chart_of_accounts: 계정과목 목록

        Returns:
            계정과목 목록
        """

    @abstractmethod
    def find_chart_of_accounts(self, user_id: int) -> list[ChartOfAccount]:
        """
        유저의 계정과목 목록 조회

        Args:
            user_id: 유저 ID

        Returns:
            계정과목 목록
        """

    @abstractmethod
    def find_chart_of_account_by_code(self, user_id: int, code: str) -> ChartOfAccount | None:
        """
        유저의 계정과목 상세 조회

        Args:
            user_id: 유저 ID
            code: 계정과목 코드

        Returns:
            계정과목 | None
        """

    @abstractmethod
    def modify_chart_of_account(self, user_id: int, code: str, updates: dict[str, Any]) -> ChartOfAccount:
        """
        유저의 계정과목 수정 (비활성화 포함)

        Args:
            user_id: 유저 ID
            code: 계정과목 코드
            updates: 수정할 속성과 값

        Returns:
            계정과목
        """
