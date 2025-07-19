import logging
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from personal_cpa.adapter.inbound.api.model.chart_of_account import (
    ChartOfAccountResponse,
    ChartOfAccountSummaryResponse,
    CreateChartOfAccountRequest,
    UpdateChartOfAccountRequest,
)
from personal_cpa.application.port.input.command.chart_of_account import (
    CreateChartOfAccountCommand,
    UpdateChartOfAccountCommand,
)
from personal_cpa.application.port.input.use_case.chart_of_account import (
    ManageChartOfAccountUseCase,
    SearchChartOfAccountUseCase,
)
from personal_cpa.container import Container

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chart_of_accounts", tags=["chart_of_accounts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=list[ChartOfAccountResponse])
@inject
async def create_chart_of_account(
    requests: list[CreateChartOfAccountRequest],
    create_chart_of_account_use_case: Annotated[
        ManageChartOfAccountUseCase, Depends(Provide[Container.chart_of_account_service])
    ],
):
    """
    유저의 계정과목 생성

    Args:
        requests: 계정과목 생성 요청 목록
        create_chart_of_account_use_case: 계정과목 생성 유즈케이스

    Returns:
        계정과목 목록

    Raises:
        HTTPException: 계정과목 생성 요청이 유효하지 않을 경우 발생
    """
    if not requests:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    try:
        commands = [
            CreateChartOfAccountCommand(
                code=request.code,
                name=request.name,
                category=request.get_category_enum(),
                description=request.description,
                parent_code=request.parent_code,
            )
            for request in requests
        ]
    except ValueError as value_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(value_error)) from value_error

    # TODO: user 개발 전까지는 1(master user)로 고정
    user_id = 1

    try:
        chart_of_accounts = create_chart_of_account_use_case.create_chart_of_accounts(user_id, commands)
    except ValueError as value_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(value_error)) from value_error
    else:
        return chart_of_accounts


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ChartOfAccountSummaryResponse])
@inject
async def get_chart_of_accounts(
    search_chart_of_account_use_case: Annotated[
        SearchChartOfAccountUseCase, Depends(Provide[Container.chart_of_account_service])
    ],
):
    """
    유저의 모든 계정과목 목록 조회

    Args:
        search_chart_of_account_use_case: 계정과목 조회 유즈케이스

    Returns:
        계정과목 트리 목록
    """
    # TODO: user 개발 전까지는 1(master user)로 고정
    user_id = 1
    return search_chart_of_account_use_case.get_chart_of_accounts(user_id)


@router.get("/{code}", status_code=status.HTTP_200_OK, response_model=ChartOfAccountResponse)
@inject
async def get_chart_of_account_by_code(
    code: str,
    search_chart_of_account_use_case: Annotated[
        SearchChartOfAccountUseCase, Depends(Provide[Container.chart_of_account_service])
    ],
):
    """
    유저의 계정과목 상세 조회

    Args:
        code: 계정과목 코드
        search_chart_of_account_use_case: 계정과목 조회 유즈케이스

    Returns:
        계정과목

    Raises:
        HTTPException: 계정과목 조회 요청이 유효하지 않을 경우 발생
    """
    # TODO: user 개발 전까지는 1(master user)로 고정
    user_id = 1

    try:
        chart_of_account = search_chart_of_account_use_case.get_chart_of_account_by_code(user_id, code)

        if not chart_of_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chart of account not found")
    except ValueError as value_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(value_error)) from value_error
    else:
        return chart_of_account


@router.put("/{code}", status_code=status.HTTP_200_OK, response_model=ChartOfAccountResponse)
@inject
async def update_chart_of_account(
    code: str,
    request: UpdateChartOfAccountRequest | None,
    update_chart_of_account_use_case: Annotated[
        ManageChartOfAccountUseCase, Depends(Provide[Container.chart_of_account_service])
    ],
):
    """
    유저의 계정과목 수정

    Args:
        code: 계정과목 코드
        request: 계정과목 수정 요청
        update_chart_of_account_use_case: 계정과목 수정 유즈케이스

    Returns:
        계정과목

    Raises:
        HTTPException: 계정과목 수정 요청이 유효하지 않을 경우 발생
    """
    if request is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    command = UpdateChartOfAccountCommand(
        name=request.name, is_hidden=request.is_hidden, description=request.description
    )

    # TODO: user 개발 전까지는 1(master user)로 고정
    user_id = 1
    return update_chart_of_account_use_case.update_chart_of_account(user_id, code, command)
