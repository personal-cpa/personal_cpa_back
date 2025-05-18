from dependency_injector import containers, providers

from personal_cpa.core.config import AppSettings
from personal_cpa.infrastructure.database import Database


class Container(containers.DeclarativeContainer):
    """
    Application의 의존성 주입 컨테이너
    """

    app_settings = providers.Singleton(AppSettings)
    database = providers.Singleton(Database, app_settings)
