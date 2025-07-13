import logging

from personal_cpa.application.port.input.command.chart_of_account import (
    CreateChartOfAccountCommand,
    UpdateChartOfAccountCommand,
)
from personal_cpa.application.port.input.use_case.chart_of_account import (
    ManageChartOfAccountUseCase,
    SearchChartOfAccountUseCase,
)
from personal_cpa.application.port.output.chart_of_account import ChartOfAccountPort
from personal_cpa.domain.chart_of_account import ChartOfAccount, ChartOfAccountTree
from personal_cpa.domain.enum.chart_of_account import AccountType

logger = logging.getLogger(__name__)


class ChartOfAccountService(SearchChartOfAccountUseCase, ManageChartOfAccountUseCase):
    """
    계정과목 서비스
    """

    def __init__(self, chart_of_account_port: ChartOfAccountPort):
        """
        초기화

        Args:
            chart_of_account_port: 계정과목 저장소
        """
        self.chart_of_account_port = chart_of_account_port

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
        chart_of_accounts = []

        for command in commands:
            _ = self._assert_chart_of_account_exists(user_id, command.code)

            parent_chart_of_account_id = None
            if command.parent_code:
                parent_chart_of_account = self._assert_parent_chart_of_account_exists(
                    user_id, command.category, command.code, command.parent_code
                )
                parent_chart_of_account_id = parent_chart_of_account.id

            chart_of_accounts.append(
                ChartOfAccount(
                    user_id=user_id,
                    code=command.code,
                    name=command.name,
                    category=command.category,
                    description=command.description,
                    parent_chart_of_account_id=parent_chart_of_account_id,
                )
            )

        return self.chart_of_account_port.save_chart_of_accounts(chart_of_accounts)

    def get_chart_of_accounts(self, user_id: int) -> list[ChartOfAccountTree]:
        """
        유저의 계정과목 목록 조회

        Args:
            user_id: 유저 ID

        Returns:
            계정과목 트리 목록
        """
        chart_of_accounts = self.chart_of_account_port.find_chart_of_accounts(user_id)

        return self._build_account_tree(chart_of_accounts)

    def get_chart_of_account_by_code(self, user_id: int, code: str) -> ChartOfAccount | None:
        """
        유저의 계정과목 상세 조회

        Args:
            user_id: 유저 ID
            code: 계정과목 코드

        Returns:
            계정과목 | None
        """
        return self.chart_of_account_port.find_chart_of_account_by_code(user_id, code)

    def update_chart_of_account(self, user_id: int, code: str, command: UpdateChartOfAccountCommand) -> ChartOfAccount:
        """
        유저의 계정과목 수정

        Args:
            user_id: 유저 ID
            code: 계정과목 코드
            command: 계정과목 수정 명령

        Raises:
            NotImplementedError: 이 기능은 아직 구현되지 않았습니다.
        """
        raise NotImplementedError("This feature is not implemented yet")

    def _build_account_tree(self, chart_of_accounts: list[ChartOfAccount]) -> list[ChartOfAccountTree]:
        """
        계정과목 트리 구축

        Args:
            chart_of_accounts: 계정과목 목록

        Returns:
            계정과목 트리 목록
        """
        account_maps = {
            account.id: ChartOfAccountTree(
                user_id=account.user_id,
                code=account.code,
                name=account.name,
                category=account.category,
                description=account.description,
                parent_chart_of_account_id=account.parent_chart_of_account_id,
                children=[],
            )
            for account in chart_of_accounts
            if not account.is_hidden
        }

        roots = []
        for account in account_maps.values():
            if account.parent_chart_of_account_id is None:
                roots.append(account)
            else:
                parent = account_maps.get(account.parent_chart_of_account_id, None)
                if parent:
                    parent.children.append(account)

        return roots

    def _assert_chart_of_account_exists(self, user_id: int, code: str) -> None:
        """
        계정과목 존재 여부 검사

        검사항목
            1. 이미 존재하는 계정과목인지 검사

        Args:
            user_id: 유저 ID
            code: 계정과목 코드

        Raises:
            ValueError: 계정과목이 존재하지 않을 경우 발생
        """
        chart_of_account = self.chart_of_account_port.find_chart_of_account_by_code(user_id, code)
        if chart_of_account:
            raise ValueError(f"Chart of account with code {code} already exists.")

    def _assert_parent_chart_of_account_exists(
        self, user_id: int, category: AccountType, code: str, parent_code: str
    ) -> ChartOfAccount:
        """
        상위 계정과목 존재 여부 검사

        검사항목
            1. 상위 계정과목 코드가 유효한지 검사
            2. 현재 계정과목 카테고리와 상위 계정과목 카테고리가 일치하는지 검사
            3. 현재 계정과목 코드가 상위 계정과목 코드로 시작하는지 검사
            4. 상위 계정과목이 숨겨져 있지 않은지 검사

        Args:
            user_id: 유저 ID
            category: 계정과목 유형
            code: 계정과목 코드
            parent_code: 상위 계정과목 코드

        Returns:
            ChartOfAccount: 상위 계정과목

        Raises:
            ValueError: 상위 계정과목이 존재하지 않을 경우 발생
            ValueError: 상위 계정과목 카테고리와 현재 계정과목 카테고리가 일치하지 않을 경우 발생
            ValueError: 현재 계정과목 코드가 상위 계정과목 코드로 시작하지 않을 경우 발생
            ValueError: 상위 계정과목이 숨겨져 있을 경우 발생
        """
        parent_chart_of_account = self.chart_of_account_port.find_chart_of_account_by_code(user_id, parent_code)

        if not parent_chart_of_account:
            raise ValueError(f"Parent chart of account with code {parent_code} not found.")

        if category != parent_chart_of_account.category:
            raise ValueError(
                f"Parent chart of account with code {parent_code} and category {parent_chart_of_account.category} must match the current account's category {category}."
            )

        if (not code.rpartition("-")[0] == parent_code) or (not code.rpartition("_")[0] == parent_code):
            raise ValueError(
                f"Parent chart of account with code {parent_code} must be a prefix of the current account's code {code}."
            )

        if parent_chart_of_account.is_hidden:
            raise ValueError(f"Parent chart of account with code {parent_code} is hidden.")

        return parent_chart_of_account
