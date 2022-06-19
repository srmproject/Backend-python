from pydantic import BaseModel
from typing import List


class RequestGetProject(BaseModel):
    """프로젝트 조회 요청"""
    user_id: int = 1  # 테스트 user_id
    name: str

class ResponseGetProject(BaseModel):
    """프로젝트 단일조회 응답"""
    id: str
    name: str
    error_detail: str

class ProjectInfo(BaseModel):
    id: str
    name: str

class ResponseGetProjects(BaseModel):
    """프로젝트 전체조회 응답"""
    results: List[ProjectInfo]
    error_detail: str

class RequestCreateProject(BaseModel):
    """프로젝트 생성 요청"""
    user_id: int = 1  # 테스트 user_id
    name: str

class ResponseCreateProject(BaseModel):
    """프로젝트 생성 응답"""
    name: str
    error_detail: str

class RequestDeleteProject(BaseModel):
    """프로젝트 삭제 요청"""
    user_id: int = 1  # 테스트 user_id
    name: str

class ResponseDeleteProject(BaseModel):
    """프로젝트 삭제 응답"""
    name: str
    error_detail: str