from abc import ABC, abstractmethod

from personal_cpa.application.port.input.command.chart_of_account import (
    CreateChartOfAccountCommand,
    UpdateChartOfAccountCommand,
)
from personal_cpa.domain.chart_of_account import ChartOfAccount, ChartOfAccountTree


class SearchChartOfAccountUseCase(ABC):
    """
    계정과목 조회 유즈케이스
    """

    @abstractmethod
    def get_chart_of_accounts(self, user_id: int) -> list[ChartOfAccountTree]:
        """
        유저의 계정과목 목록 조회

        Args:
            user_id: 유저 ID

        Returns:
            계정과목 트리 목록
        """

    @abstractmethod
    def get_chart_of_account_by_code(self, user_id: int, code: str) -> ChartOfAccount | None:
        """
        유저의 계정과목 상세 조회

        Args:
            user_id: 유저 ID
            code: 계정과목 코드

        Returns:
            계정과목 | None
        """


class ManageChartOfAccountUseCase(ABC):
    """
    계정과목 관리 유즈케이스
    """

    @abstractmethod
    def create_chart_of_accounts(
        self, user_id: int, commands: list[CreateChartOfAccountCommand]
    ) -> list[ChartOfAccount]:
        """
        유저의 계정과목 생성 (여러 개)

        Args:
            user_id: 유저 ID
            commands: 계정과목 생성 Command 목록

        Returns:
            계정과목 목록
        """

    @abstractmethod
    def update_chart_of_account(self, user_id: int, code: str, command: UpdateChartOfAccountCommand) -> ChartOfAccount:
        """
        유저의 계정과목 수정 (비활성화 포함)

        Args:
            user_id: 유저 ID
            code: 계정과목 코드
            command: 계정과목 수정 Command

        Returns:
            계정과목
        """
