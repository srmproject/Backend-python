from sqlalchemy.orm import Session
from domain.job import schemas
from sqlalchemy import text
from logger import log


def create_job(request: schemas.RequestCreateJob, db: Session):
    """job 생성"""
    statement = text("""
    INSERT INTO 
        jobs (project_id, name, description, github_url, github_branch, github_runfile, lang_type, lang_version, created_at, updated_at) 
        VALUES(:project_id, :name, :description, :github_url, :github_branch, :github_runfile, :lang_type, :lang_version, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)
    db.execute(statement, {
        "project_id": request.project_id,
        "name": request.job_name,
        "description": request.job_description,
        "github_url": request.github.url,
        "github_branch": request.github.branch,
        "github_runfile": request.github.runfile,
        "lang_type": request.lang_type,
        "lang_version": request.lang_version
    })
    db.commit()
    log.info(f"create job success: {request.job_name}")


def get_jobs(db: Session):
    """job 전체 조회"""

    statement = text("""
    SELECT (project_id, name, description, github_url, github_branch, github_runfile, lang_type, lang_version, created_at, updated_at)
        FROM jobs  
    """)
    rows = db.execute(statement, {})
    return rows
