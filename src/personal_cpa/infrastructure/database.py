from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from personal_cpa.core.config import AppSettings


class Database:
    """
    SqlAlchemy based database class
    """

    def __init__(self, app_settings: AppSettings):
        """
        Args:
            app_settings: app settings
        """
        self._engine = create_engine(
            app_settings.database_url,
            pool_size=app_settings.DB_POOL_CONNECTION_LIMIT,
            max_overflow=app_settings.DB_POOL_MAX_IDLE,
            pool_timeout=app_settings.DB_POOL_IDLE_TIMEOUT,
            pool_pre_ping=True,
            echo=True,
        )
        self._session_factory = sessionmaker(bind=self._engine, autoflush=False)
        self._session_scoped = scoped_session(self._session_factory)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Example:
            ```python
            with db.session() as session:
                result = session.query(User).all()
                # 작업 수행
                session.commit()  # 필요시 명시적 커밋
            ```

        Yields:
            Session: SQLAlchemy 세션 인스턴스

        Raises:
            Exception: 세션 사용 중 발생한 모든 예외. 예외 발생 시 세션은 롤백됩니다.
        """
        session: Session = self._session_factory()

        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
