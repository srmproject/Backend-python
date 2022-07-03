from pydantic import BaseModel
from typing import Union


class GithubFromRequestCreateJob(BaseModel):
    """job 생성할 때 사용하는 github 정보"""

    url: str
    branch: str
    runfile: str

class RequestCreateJob(BaseModel):
    """job 생성 요청"""

    user_id: str
    project_id: str
    job_name: str
    job_description: Union[str, None] = None
    lang_type: str
    lang_version: str

    github: GithubFromRequestCreateJob

class ResponseCreateJob(BaseModel):
    """프로젝트 단일조회 응답"""

    user_id: str
    project_name: str
    job_name: str
    error_detail: str
