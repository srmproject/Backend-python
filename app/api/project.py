from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from db_session import get_db
from domain.project.schemas import (
    RequestCreateProject
)
from domain.project.service import createProject


router = APIRouter(
    prefix="/api/v1/project",
    tags=["project"]
)

@router.get("/")
async def project():
    """프로젝트 조회"""  
    return {"msg": "get"}

@router.post("/create", status_code=201)
async def create(
    request: RequestCreateProject, db: Session = Depends(get_db)
    ):
    """프로젝트 생성"""
    createProject(request=request, db=db)
    return {"msg": "success"}
