from domain.project.schemas import (
    RequestCreateProject
)
from module.k8s import JCPK8S


def createProject(request: RequestCreateProject, db):
    '''프로젝트 생성'''
    k8s = JCPK8S()
    k8s.createNamspace(request.name)
