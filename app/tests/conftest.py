import pytest
from sqlalchemy import create_engine
from config import cnf
from sqlalchemy.orm import Session


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    SQLALCHEMY_DATABASE_URL = f"postgresql://{cnf.POSTGRESQL_USER}:{cnf.POSTGRESQL_PASSWORD}@{cnf.POSTGRESQL_HOST}/{cnf.POSTGRESQL_DB}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

    yield engine

@pytest.fixture(scope="function", autouse=True)
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    db = Session(bind=connection)
    yield db

    db.rollback()
    # 테스트 중 DB에 반영하고 싶으면 주석 해제
    # transaction.commit()
    connection.close()
