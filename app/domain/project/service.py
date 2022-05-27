from fastapi import status
from kubernetes.client.exceptions import ApiException
from domain.project.schemas import (
    RequestCreateProject,
    ResponseCreateProject
)
from logger import log
from module.k8s import JCPK8S


class ProjectManager:
    def createProject(self, request: RequestCreateProject, db) -> (int, ResponseCreateProject):
        """
        프로젝트 생성

        :params
          request: 사용자 요청 파라미터
          db: db 세션

        :return
        bool
            True: 프로젝트 생성 성공
            False: 프로젝트 생성 실패
        """
        k8s = JCPK8S()

        if not self.createProjectValid(namespace=request.name):
            return False

        # 쿠버네티스 namespace 생성
        try:
            k8s.createNamspace(name=request.name)
        except ApiException as e:
            if e.status == 409:
                log.error(f"[프로젝트 생성 오류] k8s namespace {request.name}이 이미 존재합니다.")
                return status.HTTP_409_CONFLICT, \
                       ResponseCreateProject(
                           name=request.name,
                           error_detail=f"{request.name}이 이미 존재합니다."
                       )

            log.error(f"[프로젝트 생성 오류] k8s namespace {request.name} 기타 생성오류: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   ResponseCreateProject(
                       name=request.name,
                       error_detail=str(e)
                   )

        # github repo 생성
        # createRepo(repo_name=request.name, token=request.github_token)

        # db 업데이트
        # try:
        #     project_crud.createProject(request=request, db=db)
        # except Exception as e:
        #     log.error("db Error")

        return status.HTTP_201_CREATED, \
               ResponseCreateProject(
                   name=request.name,
                   error_detail=""
               )

    def createProjectValid(self, namespace:str) -> bool:
        """
        프로젝트 생성 유효성 검사
          ① k8s namespace 확인

        :params
          namespace: 생성할 쿠버네티스 namespace

        :return
          bool
            True: 유효성 검사 성공
            False: 유효성 검사 실패
        """

        return self.isExistK8sNamespace(namespace=namespace)

    def isExistK8sNamespace(self, namespace) -> bool:
        """
        쿠버네티스 namespace 있는지 확인

        :params
          namespace: 생성할 쿠버네티스 namespace

        :return
          bool
            True: namespace 존재
            False: namespace 미존재
        """
        return True
