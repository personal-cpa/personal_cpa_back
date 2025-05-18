"""
Database 클래스 테스트 모듈.

이 모듈은 SQLAlchemy 기반 Database 클래스의 기능을 테스트합니다.
데이터베이스 연결, 세션 관리, CRUD 작업 및 트랜잭션 관리 등의 기능을 검증합니다.
"""

from unittest.mock import patch

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from personal_cpa.core.config import AppSettings
from personal_cpa.infrastructure.database import Database

# 테스트용 Base 모델
Base = declarative_base()


class User(Base):
    """
    테스트를 위한 사용자 모델 클래스.

    SQLAlchemy ORM을 사용하여 정의된 기본 테스트 모델로,
    데이터베이스 CRUD 작업을 검증하는 데 사용됩니다.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)


@pytest.fixture
def app_settings():
    """
    테스트에 사용할 애플리케이션 설정 객체를 제공합니다.

    애플리케이션의 실제 설정 파일에서 로드된 설정을 사용하며,
    데이터베이스 연결 및 풀 구성 설정이 포함됩니다.

    Returns:
        AppSettings: 애플리케이션 설정 객체
    """
    return AppSettings()


@pytest.fixture
def db(app_settings):
    """
    테스트에 사용할 데이터베이스 인스턴스를 제공합니다.

    Database 클래스의 인스턴스를 생성하고, 테스트 모델의 테이블을 생성합니다.
    테스트 종료 후에는 테이블을 삭제하여 데이터베이스를 정리합니다.

    Args:
        app_settings: 애플리케이션 설정 객체

    Yields:
        Database: 데이터베이스 인스턴스
    """
    database = Database(app_settings)

    # 테스트용 테이블 생성
    Base.metadata.create_all(database._engine)

    yield database

    # 테스트 후 테이블 삭제
    Base.metadata.drop_all(database._engine)


def test_database_init(app_settings):
    """
    Database 클래스의 초기화 과정을 테스트합니다.

    create_engine 함수가 올바른 매개변수로 호출되는지 검증합니다.
    이 테스트는 SQLAlchemy 엔진이 애플리케이션 설정에 따라
    올바르게 구성되는지 확인합니다.

    Args:
        app_settings: 애플리케이션 설정 객체
    """
    with patch("personal_cpa.infrastructure.database.create_engine") as mock_create_engine:
        Database(app_settings)

        mock_create_engine.assert_called_once_with(
            app_settings.database_url,
            pool_size=app_settings.DB_POOL_CONNECTION_LIMIT,
            max_overflow=app_settings.DB_POOL_MAX_IDLE,
            pool_timeout=app_settings.DB_POOL_IDLE_TIMEOUT,
            pool_pre_ping=True,
            echo=True,
        )


def test_session_creation(db):
    """
    세션 컨텍스트 매니저를 통한 세션 생성을 테스트합니다.

    db.session() 컨텍스트 매니저가 유효한 SQLAlchemy 세션 객체를 제공하는지,
    그리고 그 세션이 올바른 엔진에 바인딩되어 있는지 검증합니다.

    Args:
        db: 데이터베이스 인스턴스
    """
    with db.session() as session:
        assert isinstance(session, Session)
        # 세션이 작동하는지 확인
        assert session.bind == db._engine


def test_session_crud_operations(db):
    """
    세션을 사용한 기본 CRUD 작업을 테스트합니다.

    User 모델을 사용하여 생성(Create), 읽기(Read),
    업데이트(Update), 삭제(Delete) 작업이 올바르게
    수행되는지 검증합니다.

    Args:
        db: 데이터베이스 인스턴스
    """
    # 사용자 추가
    with db.session() as session:
        user = User(name="Test User", email="test@example.com")
        session.add(user)
        session.commit()

    # 사용자 조회
    with db.session() as session:
        user = session.query(User).filter_by(email="test@example.com").first()
        assert user is not None
        assert user.name == "Test User"

        # 사용자 업데이트
        user.name = "Updated User"
        session.commit()

    # 업데이트 확인
    with db.session() as session:
        user = session.query(User).filter_by(email="test@example.com").first()
        assert user.name == "Updated User"

        # 사용자 삭제
        session.delete(user)
        session.commit()

    # 삭제 확인
    with db.session() as session:
        user = session.query(User).filter_by(email="test@example.com").first()
        assert user is None


def test_session_rollback_on_exception(db):
    """
    예외 발생 시 세션 롤백 기능을 테스트합니다.

    세션 컨텍스트 매니저가 예외 발생 시 트랜잭션을 올바르게
    롤백하는지 확인합니다. 고유 제약 조건 위반과 같은
    데이터베이스 에러 상황에서 일관성을 유지하는지 검증합니다.

    Args:
        db: 데이터베이스 인스턴스
    """
    # 첫 번째 사용자 추가
    with db.session() as session:
        user = User(name="Test User", email="test@example.com")
        session.add(user)
        session.commit()

    # 중복 이메일로 예외 발생 시나리오
    try:
        with db.session() as session:
            # 같은 이메일을 가진 사용자 추가 시도 (unique 제약 조건 위반)
            duplicate_user = User(name="Another User", email="test@example.com")
            session.add(duplicate_user)
            session.commit()  # 여기서 예외 발생
    except Exception:
        pass  # 예외는 예상된 것이므로 무시

    # 롤백 확인: 데이터베이스에 변경이 없어야 함
    with db.session() as session:
        users = session.query(User).all()
        assert len(users) == 1
        assert users[0].name == "Test User"


def test_session_close(db):
    """
    세션이 항상 닫히는지 테스트합니다.

    세션 컨텍스트 매니저가 정상 종료 및 예외 발생 상황 모두에서
    세션을 올바르게 닫는지 검증합니다. 이는 리소스 누수를
    방지하기 위한 중요한 기능입니다.

    Args:
        db: 데이터베이스 인스턴스
    """
    with patch.object(Session, "close") as mock_close:
        try:
            with db.session() as session:
                # 세션 사용
                pass
        finally:
            # 성공적으로 완료되었을 때 세션이 닫히는지 확인
            mock_close.assert_called_once()

        mock_close.reset_mock()

        try:
            with db.session() as session:
                # 예외 발생
                raise ValueError("Test exception")
        except ValueError:
            # 예외가 발생했을 때도 세션이 닫히는지 확인
            mock_close.assert_called_once()


def test_scoped_session(db):
    """
    스코프드 세션 기능을 테스트합니다.

    스코프드 세션이 동일한 스레드 내에서 같은 세션 인스턴스를
    반환하는지 확인하고, 세션 제거 후에는 새로운 세션 인스턴스를
    생성하는지 검증합니다. 스코프드 세션은 스레드당 하나의
    세션을 유지하는 SQLAlchemy의 중요한 기능입니다.

    Args:
        db: 데이터베이스 인스턴스
    """
    # 같은 스레드에서는 동일한 세션 반환
    session1 = db._session_scoped()
    session2 = db._session_scoped()

    assert session1 is session2  # 동일한 객체인지 확인

    # 스코프드 세션 사용
    user = User(name="Scoped User", email="scoped@example.com")
    session1.add(user)
    session1.commit()

    # 다른 세션에서 조회 (스코프드 세션이므로 같은 세션)
    user_from_db = session2.query(User).filter_by(email="scoped@example.com").first()
    assert user_from_db is not None
    assert user_from_db.name == "Scoped User"

    # 세션 제거
    db._session_scoped.remove()

    # 제거 후 새 세션 생성
    session3 = db._session_scoped()
    assert session1 is not session3  # 다른 객체인지 확인
