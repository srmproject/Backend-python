from fastapi import APIRouter

router = APIRouter(
    prefix="/project",
    tags=["project"]
)

@router.get("/")
async def project():
    """프로젝트 조회"""
    return {"msg": "get"}

@router.post("/create")
async def create():
    """프로젝트 생성"""
    return {"msg": "create"}

