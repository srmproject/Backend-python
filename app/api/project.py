from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db_session import get_db
from domain.project.schemas import (
    RequestCreateProject
)
from domain.project.service import ProjectManager
from logger import log

router = APIRouter(
    prefix="/api/v1/project",
    tags=["project"]
)

@router.get("/")
async def project():
    """프로젝트 조회"""  
    return {"msg": "get"}

@router.post("/create")
async def create(
    request: RequestCreateProject, db: Session = Depends(get_db)
    ):
    """프로젝트 생성"""
    log.info("============= /project/create is called ============= ")
    project_manager = ProjectManager()
    try:
        status_code, detail = project_manager.createProject(request=request, db=db)
    except Exception as e:
        log.error(f"[프로젝트 생성 서비스 호출오류] 예기치 못한 오류: {e}")
        return JSONResponse(
            status_code=500,
            content=""
        )

    return JSONResponse(
        status_code=status_code,
        content=dict(detail)
    )
