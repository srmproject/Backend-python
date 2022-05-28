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
            projects (name, created_at, updated_at) 
            VALUES(:name, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)
        """)
        db.execute(statement, {
            "name": request.name
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


