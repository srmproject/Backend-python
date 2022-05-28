from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db_session import get_db
from domain.project.schemas import (
    RequestCreateProject,
    RequestDeleteProject
)
from domain.project.service import ProjectManager
from logger import log

router = APIRouter(
    prefix="/api/v1/project",
    tags=["project"]
)

@router.get("/")
async def project(
    name: str = None, db: Session = Depends(get_db)
    ):
    """프로젝트 조회"""
    log.info("============= /project/ is called ============= ")
    project_manager = ProjectManager()

    if name is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="이름을 입력하지 않았습니다"
        )

    try:
        status_code, detail = project_manager.getProject(namespace=name, db=db)
    except Exception as e:
        log.error(f"[프로젝트 조회 서비스 호출오류] 예기치 못한 오류: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=""
        )

    return JSONResponse(
        status_code=status_code,
        content=dict(detail)
    )

@router.post("/")
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=""
        )

    return JSONResponse(
        status_code=status_code,
        content=dict(detail)
    )

@router.delete("/")
async def delete(
    request: RequestDeleteProject, db: Session = Depends(get_db)
    ):
    """
    프로젝트 삭제
    :param request: 사용자 삭제요청
    :param db: db 세션
    :return:
    """
    log.info("============= /project/delete is called ============= ")
    project_manager = ProjectManager()
    try:
        status_code, detail = project_manager.deleteProject(request=request, db=db)
    except Exception as e:
        log.error(f"[프로젝트 삭제 서비스 호출오류] 예기치 못한 오류: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="프로젝트 삭제 실패"
        )

    return JSONResponse(
        status_code=status_code,
        content=dict(detail)
    )