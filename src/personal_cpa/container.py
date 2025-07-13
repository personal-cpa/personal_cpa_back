from dependency_injector import containers, providers

from personal_cpa.adapter.outbound.database.repository.chart_of_account import ChartOfAccountRepository
from personal_cpa.application.service.chart_of_account import ChartOfAccountService
from personal_cpa.config import AppSettings
from personal_cpa.database import Database


class Container(containers.DeclarativeContainer):
    """
    애플리케이션의 의존성 주입 컨테이너
    """

    app_settings = providers.Singleton(AppSettings)

    database = providers.Singleton(Database, app_settings=app_settings)

    chart_of_account_repository = providers.Factory(ChartOfAccountRepository, session_factory=database.provided.session)

    chart_of_account_service = providers.Factory(
        ChartOfAccountService, chart_of_account_port=chart_of_account_repository
    )
