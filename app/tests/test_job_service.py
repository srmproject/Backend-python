from domain.job import (
    schemas,
    service
)
import pytest
from fastapi import HTTPException


def test_create_job_failed_no_project(db):
    """프로젝트가 없어 job생성 실패"""

    unvalid_project = "1"
    request_body = schemas.RequestCreateJob(
        user_id="1",
        project_id=unvalid_project,
        job_name="pytest-job",
        job_description="",
        lang_type="",
        lang_version="",
        github=schemas.GithubFromRequestCreateJob(
            url="https://github.com/srmproject/docker_images.git",
            branch="main",
            runfile="jobs/sample/helloworld.sh"
        )
    )
    jcp_job_manager = service.JobManager()
    with pytest.raises(HTTPException):
        jcp_job_manager.create_job(request=request_body, db=db)

def test_create_job_failed_unavailable_job_name(db):
    """job name에 '_'가 포함되어 job생성 실패"""

    unvalid_job_name = "this_is_failed_name"
    request_body = schemas.RequestCreateJob(
        user_id="1",
        project_id="default",
        job_name=unvalid_job_name,
        job_description="",
        lang_type="",
        lang_version="",
        github=schemas.GithubFromRequestCreateJob(
            url="https://github.com/srmproject/docker_images.git",
            branch="main",
            runfile="jobs/sample/helloworld.sh"
        )
    )

    jcp_job_manager = service.JobManager()
    with pytest.raises(HTTPException):
        jcp_job_manager.create_job(request=request_body, db=db)

def test_create_job(db):
    """job 생성"""
    request_body = schemas.RequestCreateJob(
        user_id="1",
        project_id="1",
        job_name="test1-pytest-1",
        job_description="",
        lang_type="",
        lang_version="",
        github=schemas.GithubFromRequestCreateJob(
            url="https://github.com/srmproject/docker_images.git",
            branch="main",
            runfile="jobs/sample/helloworld.sh"
        )
    )

    jcp_job_manager = service.JobManager()
    jcp_job_manager.create_job(request=request_body, db=db)

def test_create_job_failed_duplicate_name(db):
    """job name 중복으로 생성 실패"""

    request_body = schemas.RequestCreateJob(
        user_id="1",
        project_id="1",
        job_name="test1-pytest-1",
        job_description="",
        lang_type="",
        lang_version="",
        github=schemas.GithubFromRequestCreateJob(
            url="https://github.com/srmproject/docker_images.git",
            branch="main",
            runfile="jobs/sample/helloworld.sh"
        )
    )

    jcp_job_manager = service.JobManager()
    jcp_job_manager.create_job(request=request_body, db=db)
    with pytest.raises(HTTPException):
        jcp_job_manager.create_job(request=request_body, db=db)
