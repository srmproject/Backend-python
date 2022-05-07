from pydantic import BaseModel


class RequestCreateProject(BaseModel):
    """프로젝트 생성 요청"""
    name: str
