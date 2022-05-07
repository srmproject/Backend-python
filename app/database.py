from sqlalchemy import create_engine
from config import cnf
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://{cnf.POSTGRESQL_USER}:{cnf.POSTGRESQL_PASSWORD}@{cnf.POSTGRESQL_HOST}/{cnf.POSTGRESQL_DB}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
