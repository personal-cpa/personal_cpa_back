from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from personal_cpa.domain.enum.chart_of_account import AccountType


class CategoryValidationMixin:
    """
    계정과목 카테고리 검증 및 변환을 위한 Mixin 클래스
    """

    category: int

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: int) -> int:
        """
        계정과목 카테고리 검증

        Args:
            value: 계정과목 카테고리

        Returns:
            int: 계정과목 카테고리

        Raises:
            ValueError: 계정과목 카테고리가 유효하지 않을 경우 발생
        """
        try:
            AccountType(value)
        except ValueError as value_error:
            raise ValueError(f"Invalid category: {value}") from value_error
        else:
            return value

    def get_category_enum(self) -> AccountType:
        """
        계정과목 카테고리 열거형 반환

        Returns:
            AccountType: 계정과목 카테고리 열거형
        """
        return AccountType(self.category)


class CreateChartOfAccountRequest(CategoryValidationMixin, BaseModel):
    """
    계정과목 생성 요청

    Args:
        code: 계정과목 코드
        name: 계정과목 이름
        category: 계정과목 카테고리
        description: 계정과목 설명
        parent_code: 상위 계정과목 코드
    """

    class Config:
        """
        모델 설정
        """

        validate_default = True

    code: str
    name: str
    category: int
    description: str | None
    parent_code: str | None = None


class ChartOfAccountResponse(BaseModel):
    """
    계정과목 응답
    """

    model_config = ConfigDict(from_attributes=True, json_encoders={AccountType: lambda v: v.name})

    code: str
    name: str
    category: AccountType = Field(
        description=f"계정과목 카테고리({', '.join([account_type.name for account_type in AccountType])})"
    )
    description: str | None
    parent_chart_of_account_id: int | None


class ChartOfAccountSummaryResponse(BaseModel):
    """
    계정과목 응답
    """

    model_config = ConfigDict(from_attributes=True, json_encoders={AccountType: lambda v: v.name})

    code: str
    name: str
    category: AccountType = Field(
        description=f"계정과목 카테고리({', '.join([account_type.name for account_type in AccountType])})"
    )
    children: list[ChartOfAccountSummaryResponse] | None


class UpdateChartOfAccountRequest(CategoryValidationMixin, BaseModel):
    """
    계정과목 수정 요청
    """

    name: str
    category: int
    is_hidden: bool
    description: str | None
