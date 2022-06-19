from sqlalchemy.orm import Session
from domain.project.schemas import (
    RequestCreateProject,
    RequestDeleteProject,
    RequestGetProject
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
        db.rollback()
        raise RuntimeError(e)
    except Exception as e:
        log.error(f"[-] other error: {e}")
        db.rollback()
        raise RuntimeError(e)

def deleteProject(request: RequestDeleteProject, db: Session):
    """프로젝트 삭제"""
    try:
        statement = text("""
        DELETE FROM projects where user_id=(:user_id) and name=(:name)
        """)
        db.execute(statement, {
            "user_id": request.user_id,
            "name": request.name
        })
        db.commit()
        log.info(f"delete project success: {request.name}")
    except exc.IntegrityError as e:
        log.error(f"[-] {e}이 project table에 없습니다.: {e}")
        db.rollback()
        raise RuntimeError(e)
    except Exception as e:
        db.rollback()
        raise RuntimeError(e)

def getProject(request: RequestGetProject, db: Session):
    """프로젝트 단일조회"""
    try:
        statement = text("""
        SELECT id, user_id, name, description 
        from projects 
        where user_id=(:user_id) and name=(:name)
        """)
        row = db.execute(statement, {
            "user_id": request.user_id,
            "name": request.project_name
        })
        log.info(f"get project success: {request.project_name}")
    except exc.IntegrityError as e:
        log.error(f"[-] {e}이 project table에 없습니다.: {e}")
        raise RuntimeError(e)
    except Exception as e:
        log.error(f"[-] other error: {e}")
        raise RuntimeError(e)
    else:
        return row

def getProjects(db: Session):
    """프로젝트 전체조회"""
    try:
        statement = text("""
        SELECT id, user_id, name, description 
        from projects
        """)
        rows = db.execute(statement, {})
        log.info(f"get projectALL success")
    except exc.IntegrityError as e:
        log.error(f"[-] {e}이 project table에 없습니다.: {e}")
        raise RuntimeError(e)
    except Exception as e:
        log.error(f"[-] other error: {e}")
        raise RuntimeError(e)
    else:
        return rows
