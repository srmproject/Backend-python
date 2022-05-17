from sqlalchemy.orm import Session
from domain.project.schemas import RequestCreateProject
from sqlalchemy import exc, text
import exceptions
from logger import getLogger


log = getLogger()

def createProject(request: RequestCreateProject, db: Session):
    '''프로젝트 생성'''
    try:
        statement = text("""
        INSERT INTO 
            projects (name, created_at, updated_at) 
            VALUES(:name, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)
        """)
        db.execute(statement, {
            "name": request.name
        })
        db.commit()
        log.info(f"create project sucess: {request.name}")
    except exc.IntegrityError as e:
        log.error(f"[-] Data is already in DB: {e}")
        db.rollback()
        raise exceptions.DBItemAlreadyExist("Data is already in DB")        
    except Exception as e:
        log.error(f"[-] other error: {e}")
        db.rollback()
        raise RuntimeError

