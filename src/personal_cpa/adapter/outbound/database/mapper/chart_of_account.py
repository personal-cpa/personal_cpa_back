from attr import dataclass

from personal_cpa.adapter.outbound.database.model.chart_of_account import ChartOfAccountEntity
from personal_cpa.domain.chart_of_account import ChartOfAccount
from personal_cpa.domain.enum.chart_of_account import AccountType


@dataclass
class ChartOfAccountMapper:
    """
    계정과목 매퍼
    """

    @staticmethod
    def to_domain(entity: ChartOfAccountEntity) -> ChartOfAccount:
        """
        계정과목 모델을 도메인 모델로 변환합니다.

        Args:
            entity: 계정과목 모델

        Returns:
            도메인 모델
        """
        return ChartOfAccount(
            user_id=entity.user_id,
            code=entity.code,
            name=entity.name,
            category=AccountType(entity.category),
            is_hidden=entity.is_hidden,
            description=entity.description,
            parent_chart_of_account_id=entity.parent_chart_of_account_id,
            id=entity.id,
        )

    @staticmethod
    def to_entity(domain: ChartOfAccount) -> ChartOfAccountEntity:
        """
        도메인 모델을 계정과목 모델로 변환합니다.

        Args:
            domain: 도메인 모델

        Returns:
            계정과목 모델
        """
        return ChartOfAccountEntity(
            id=domain.id,
            user_id=domain.user_id,
            code=domain.code,
            name=domain.name,
            category=domain.category.value,
            is_hidden=domain.is_hidden,
            description=domain.description,
            parent_chart_of_account_id=domain.parent_chart_of_account_id,
        )
