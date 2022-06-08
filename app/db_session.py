from database import SessionLocal
from logger import log


def get_db():
    '''DB 세션관리'''
    log.info("[-] db 세션생성")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        log.info("[-] db 세션 종료")
