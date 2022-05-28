from pydantic import BaseModel


class ResponseGetProject(BaseModel):
    """프로젝트 조회 응답"""
    id: str
    name: str
    error_detail: str

class RequestCreateProject(BaseModel):
    """프로젝트 생성 요청"""
    user_id: int = 1
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