from sqlalchemy.orm import Session
from domain.project.schemas import (
    RequestCreateProject,
    RequestDeleteProject
)
from sqlalchemy import exc, text
from logger import log


def createProject(request: RequestCreateProject, db: Session):
    """프로젝트 생성"""
    try:
        statement = text("""
        INSERT INTO 
            projects (name, user_id, created_at, updated_at) 
            VALUES(:name, :user_id ,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)
        """)
        db.execute(statement, {
            "name": request.name,
            "user_id": request.user_id
        })
        db.commit()
        log.info(f"create project success: {request.name}")
    except exc.IntegrityError as e:
        log.error(f"[-] Data is already in DB: {e}")
        db.rollback()
        raise RuntimeError
    except Exception as e:
        log.error(f"[-] other error: {e}")
        db.rollback()
        raise RuntimeError

def deleteProject(request: RequestDeleteProject, db: Session):
    """프로젝트 삭제"""
    try:
        statement = text("""
        DELETE FROM projects where name=(:name)
        """)
        db.execute(statement, {
            "name": request.name
        })
        db.commit()
        log.info(f"delete project success: {request.name}")
    except exc.IntegrityError as e:
        log.error(f"[-] {e}이 project table에 없습니다.: {e}")
        db.rollback()
        raise RuntimeError
    except Exception as e:
        log.error(f"[-] other error: {e}")
        db.rollback()
        raise RuntimeError

def getProject(namespace: str, db: Session):
    """프로젝트 조회"""
    try:
        statement = text("""
        SELECT id, name, description from projects where name=(:name)
        """)
        row = db.execute(statement, {
            "name": namespace
        })
        log.info(f"get project success: {namespace}")
    except exc.IntegrityError as e:
        log.error(f"[-] {e}이 project table에 없습니다.: {e}")
        raise RuntimeError
    except Exception as e:
        log.error(f"[-] other error: {e}")
        raise RuntimeError
    else:
        return row
