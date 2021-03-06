from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db_session import get_db
from domain.project.schemas import (
    RequestCreateProject,
    RequestDeleteProject,
    RequestGetProject
)
from domain.project.service import ProjectManager
from logger import log
from typing import Union


router = APIRouter(
    prefix="/api/v1",
    tags=["project"]
)

@router.get("/projects")
async def get_projects(
        user_id: Union[str, None] = None,
        db: Session = Depends(get_db)):
    """프로젝트 전체조회"""
    log.info("============= /projects is called ============= ")

    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_detail": "유저를 입력하지 않았습니다."
            }
        )

    project_manager = ProjectManager()

    try:
        status_code, detail = project_manager.get_projects_from_userid(user_id=user_id, db=db)
    except Exception as e:
        log.error(f"[프로젝트 전체조회 서비스 호출오류] 예기치 못한 오류: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=""
        )

    return JSONResponse(
        status_code=status_code,
        content=detail.dict()
    )

@router.get("/project")
async def get_project(
    project_name: Union[str, None] = None, user_id: Union[str, None] = None, db: Session = Depends(get_db)
    ):
    """프로젝트 단일조회"""
    log.info("============= /project/ is called ============= ")
    project_manager = ProjectManager()

    if project_name is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_detail": "프로젝트 이름을 입력하지 않았습니다"
            }
        )

    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_detail": "유저를 입력하지 않았습니다."
            }
        )

    request = RequestGetProject(
        project_name=project_name,
        user_id=user_id
    )

    try:
        status_code, detail = project_manager.get_project_from_userid(request=request, db=db)
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

@router.post("/project")
async def create(
    request: RequestCreateProject, db: Session = Depends(get_db)
    ):
    """프로젝트 생성"""
    log.info("============= /project/create is called ============= ")
    project_manager = ProjectManager()
    try:
        status_code, detail = project_manager.create_project(request=request, db=db)
    except Exception as e:
        log.error(f"[프로젝트 생성 서비스 호출오류] 예기치 못한 오류: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={}
        )

    return JSONResponse(
        status_code=status_code,
        content=dict(detail)
    )

@router.delete("/project")
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
        status_code, detail = project_manager.delete_project(request=request, db=db)
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
