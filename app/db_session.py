from database import SessionLocal


def get_db():
    '''DB 세션관리'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
