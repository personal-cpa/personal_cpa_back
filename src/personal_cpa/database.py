from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from personal_cpa.config import AppSettings


class Database:
    """
    데이터베이스 연결 관리
    """

    def __init__(self, app_settings: AppSettings):
        """
        초기화

        Args:
            app_settings: 애플리케이션 설정
        """
        self._engine = create_engine(
            app_settings.database_url,
            echo=True,
            pool_size=app_settings.DB_POOL_CONNECTION_LIMIT,
            max_overflow=app_settings.DB_POOL_MAX_IDLE,
            pool_timeout=app_settings.DB_POOL_IDLE_TIMEOUT,
            pool_pre_ping=True,
        )
        _session_factory = sessionmaker(bind=self._engine, expire_on_commit=False, autocommit=False, autoflush=False)
        self._session_scoped = scoped_session(_session_factory)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        세션 생성

        Yields:
            Session: 세션

        Raises:
            Exception: 세션 생성 중 오류가 발생할 경우 발생
        """
        session = self._session_scoped()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self._session_scoped.remove()
