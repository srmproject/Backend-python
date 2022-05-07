from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from db_session import get_db
from domain.project.schemas import (
    ProjectCreate,
    ResponseCreateProject
)
from domain.project.crud import (
    createProject
)

router = APIRouter(
    prefix="/api/v1/project",
    tags=["project"]
)

@router.get("/")
async def project():
    """프로젝트 조회"""  
    return {"msg": "get"}

@router.post("/create", response_model=ResponseCreateProject, status_code=201)
async def create(request: ProjectCreate, db: Session = Depends(get_db)):
    """프로젝트 생성"""
    return createProject(project=request, db=db)

