from contextlib import AbstractContextManager
from typing import Any, Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from personal_cpa.adapter.outbound.database.mapper.chart_of_account import ChartOfAccountMapper
from personal_cpa.adapter.outbound.database.model.chart_of_account import ChartOfAccountEntity
from personal_cpa.application.port.output.chart_of_account import ChartOfAccountPort
from personal_cpa.domain.chart_of_account import ChartOfAccount


class ChartOfAccountRepository(ChartOfAccountPort):
    """
    계정과목 저장소
    """

    def __init__(self, session_factory: Callable[[], AbstractContextManager[Session]]) -> None:
        """
        초기화

        Args:
            session_factory: 세션 팩토리
        """
        self.session_factory = session_factory

    def save_chart_of_accounts(self, chart_of_accounts: list[ChartOfAccount]) -> list[ChartOfAccount]:
        """
        유저의 계정과목 생성 (여러 개)

        Args:
            chart_of_accounts: 계정과목 목록

        Returns:
            계정과목 목록
        """
        entities = [ChartOfAccountMapper.to_entity(chart_of_account) for chart_of_account in chart_of_accounts]

        with self.session_factory() as session:
            session.add_all(entities)
            session.commit()

            for entity in entities:
                session.refresh(entity)

            return [ChartOfAccountMapper.to_domain(entity) for entity in entities]

    def find_chart_of_accounts(self, user_id: int) -> list[ChartOfAccount]:
        """
        유저의 계정과목 목록 조회

        Args:
            user_id: 유저 ID

        Returns:
            계정과목 목록
        """
        query = select(ChartOfAccountEntity).where(ChartOfAccountEntity.user_id == user_id)

        with self.session_factory() as session:
            result = session.execute(query)
            entities = result.scalars().all()

            return [ChartOfAccountMapper.to_domain(entity) for entity in entities]

    def find_chart_of_account_by_code(self, user_id: int, code: str) -> ChartOfAccount | None:
        """
        유저의 계정과목 상세 조회

        Args:
            user_id: 유저 ID
            code: 계정과목 코드

        Returns:
            계정과목 | None
        """
        query = (
            select(ChartOfAccountEntity)
            .where(ChartOfAccountEntity.user_id == user_id)
            .where(ChartOfAccountEntity.code == code)
        )

        with self.session_factory() as session:
            result = session.execute(query)
            entity = result.scalar_one_or_none()
            return ChartOfAccountMapper.to_domain(entity) if entity else None

    def modify_chart_of_account(self, user_id: int, code: str, updates: dict[str, Any]) -> ChartOfAccount:
        """
        유저의 계정과목 수정 (비활성화 포함)

        Args:
            user_id: 유저 ID
            code: 계정과목 코드
            updates: 수정할 속성과 값

        Returns:
            계정과목

        Raises:
            ValueError: 계정과목이 존재하지 않을 경우 발생
        """
        with self.session_factory() as session:
            entity = (
                session.query(ChartOfAccountEntity)
                .filter(ChartOfAccountEntity.user_id == user_id)
                .filter(ChartOfAccountEntity.code == code)
            ).first()

            if not entity:
                raise ValueError(f"Chart of account with id {code} not found.")

            for attr, value in updates.items():
                if value is not None:
                    setattr(entity, attr, value)

            session.commit()
            session.refresh(entity)

            return ChartOfAccountMapper.to_domain(entity)
