from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql.functions import current_timestamp

from personal_cpa.adapter.outbound.database.model.base import Base


class ChartOfAccountEntity(Base):
    """
    계정과목 모델
    """

    __tablename__ = "chart_of_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(Integer, nullable=False)
    is_hidden = Column(Boolean, nullable=False, default=False)
    description = Column(Text, nullable=True)
    parent_chart_of_account_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp(), onupdate=current_timestamp())

    def __repr__(self) -> str:
        """
        Returns:
            객체의 공식적인 문자열
        """
        return (
            f"<ChartOfAccounts("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"code={self.code}, "
            f"name={self.name}, "
            f"category={self.category}, "
            f"is_hidden={self.is_hidden}, "
            f"description={self.description}, "
            f"parent_chart_of_account_id={self.parent_chart_of_account_id}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at}"
            f")>"
        )
