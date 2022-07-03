from fastapi import APIRouter
from domain.job import (
    crud,
    schemas,
    service
)
from logger import log

router = APIRouter(
    prefix="/api/v1",
    tags=["job"]
)


@router.post("/job")
def create(request: schemas.RequestCreateJob):
    """job 생성"""
    job_manager = service.JobManager

    try:
        job_manager.create_job(request, None)
    except Exception as e:
        log.error(f"error: {e}")
