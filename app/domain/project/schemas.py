from pydantic import BaseModel


class RequestCreateProject(BaseModel):
    """프로젝트 생성 요청"""
    name: str

class ResponseCreateProject(BaseModel):
    """프로젝트 생성 응답"""
    name: str
    error_detail: str

class RequestDeleteProject(BaseModel):
    """프로젝트 삭제 요청"""
    name: str

class ResponseDeleteProject(BaseModel):
    """프로젝트 삭제 응답"""
    name: str
    error_detail: str