from pydantic import BaseModel


class RequestCreateProject(BaseModel):
    """프로젝트 생성 요청"""
    name: str
    github_token: str


class ResponseCreateProject(BaseModel):
    """프로젝트 생성 응답"""
    name: str
    error_detail: str
