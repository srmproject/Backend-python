from database import SessionLocal
from logger import log


def get_db():
    '''DB 세션관리'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
