# ruff: noqa: ERA001
import pytest

from personal_cpa.domain.chart_of_account import ChartOfAccount
from personal_cpa.domain.enum.chart_of_account import AccountType


def test_chart_of_account_valid_instance():
    """
    Test Case: 유효한 인스턴스 검사
    :return:
    """
    account = ChartOfAccount(
        user_id=1,
        name="현금",
        code="101",
        category=AccountType.ASSET,
        is_hidden=False,
        description="주계좌",
        parent_chart_of_account=None,
    )
    assert account.name == "현금"
    assert account.category == AccountType.ASSET


def test_chart_of_account_empty_name_raises_value_error():
    """
    Test Case: 이름 공백 검사
    :return:
    """
    with pytest.raises(ValueError, match="name is not empty"):
        ChartOfAccount(
            user_id=1,
            name="   ",
            code="101",
            category=AccountType.ASSET,
            is_hidden=False,
            description=None,
            parent_chart_of_account=None,
        )


def test_chart_of_account_empty_code_raises_value_error():
    """
    Test Case: code 공백 검사
    """
    with pytest.raises(ValueError, match="code is not empty"):
        ChartOfAccount(
            user_id=1,
            name="현금",
            code="",
            category=AccountType.ASSET,
            is_hidden=False,
            description=None,
            parent_chart_of_account=None,
        )


def test_chart_of_account_invalid_type_raises_type_error():
    """
    Test Case: AccountType type 검사
    :return:
    """
    with pytest.raises(TypeError, match="type must be an AccountType enum"):
        ChartOfAccount(  # pyright: ignore[reportArgumentType]
            user_id=1,
            name="현금",
            code="101",
            category="ASSET",  # 잘못된 타입
            is_hidden=False,
            description=None,
            parent_chart_of_account=None,
        )


def test_chart_of_account_invalid_code_character_raises_value_error():
    """
    Test Case: number 유효성 검사
    :return:
    """
    with pytest.raises(ValueError, match="code can only be a number OR"):
        ChartOfAccount(
            user_id=1,
            name="현금",
            code="10A1",  # 'A'는 허용되지 않음
            category=AccountType.ASSET,
            is_hidden=False,
            description=None,
            parent_chart_of_account=None,
        )


def test_chart_of_account_parent_type_mismatch_raises_value_error():
    """
    Test Case: 부모 AccountType 일치 검사
    :return:
    """
    parent = ChartOfAccount(
        user_id=1,
        name="부채계정",
        code="200",
        category=AccountType.LIABILITY,
        is_hidden=False,
        description=None,
        parent_chart_of_account=None,
    )
    with pytest.raises(ValueError, match="must match"):
        ChartOfAccount(
            user_id=1,
            name="현금",
            code="101",
            category=AccountType.ASSET,
            is_hidden=False,
            description=None,
            parent_chart_of_account=parent,
        )


# def test_chart_of_account_parent_type_match_ok():
#     parent = ChartOfAccount(
#         user_id=1,
#         name="자산계정",
#         code="100",
#         type=AccountType.ASSET,
#         is_hidden=False,
#         description=None,
#         parent_chart_of_account=None
#     )
#     child = ChartOfAccount(
#         user_id=1,
#         name="현금",
#         code="101",
#         type=AccountType.ASSET,
#         is_hidden=False,
#         description=None,
#         parent_chart_of_account=parent
#     )
#     assert child.parent_chart_of_account == parent
