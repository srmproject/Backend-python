from fastapi import status
from kubernetes.client.exceptions import ApiException
from domain.project.schemas import (
    RequestCreateProject,
    ResponseCreateProject,
    RequestDeleteProject,
    ResponseDeleteProject,
    ResponseGetProject
)
import domain.project.crud as project_crud
from logger import log
from module.k8s import JCPK8S


class ProjectManager:
    def createProject(self, request: RequestCreateProject, db) -> (int, ResponseCreateProject):
        """프로젝트 생성"""
        k8s = JCPK8S()

        if not self.createProjectValid(namespace=request.name):
            return False

        # 쿠버네티스 namespace 생성
        try:
            k8s.createNamespace(namespace=request.name)
        except ApiException as e:
            if e.status == 409:
                log.error("[프로젝트 생성 오류] k8s namespace {request.name}이 이미 존재합니다")
                return status.HTTP_409_CONFLICT, \
                       ResponseCreateProject(
                           name=request.name,
                           error_detail=f"{request.name}이 이미 존재합니다."
                       )

            log.error(f"[프로젝트 생성 오류] k8s namespace {request.name} 기타 생성오류: {e.status}. {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   ResponseCreateProject(
                       name=request.name,
                       error_detail=str(e)
                   )

        # github repo 생성
        # createRepo(repo_name=request.name, token=request.github_token)

        # db 업데이트
        try:
            project_crud.createProject(request=request, db=db)
        except Exception as e:
            db_error_code = e.args[0].orig.pgcode
            if db_error_code == "23503":
                log.error(f"[프로젝트 생성 오류] 데이터베이스 오류: user_id가 존재하지 않음 {db_error_code}->{e}")
            else:
                log.error(f"[프로젝트 생성 오류] 데이터베이스 오류: 기타에러 {e.args[0].code}->{e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   ResponseCreateProject(
                       name=request.name,
                       error_detail="프로젝트 생성을 실패했습니다."
                   )

        return status.HTTP_201_CREATED, \
               ResponseCreateProject(
                   name=request.name,
                   error_detail=""
               )

    def deleteProject(self, request: RequestDeleteProject, db) -> (int, ResponseDeleteProject):
        """프로젝트 삭제"""
        k8s = JCPK8S()

        # 쿠버네티스 네임스페이스 삭제
        try:
            k8s.deleteNamespace(namespace=request.name)
        except ApiException as e:
            pass

        # DB행 삭제
        try:
            project_crud.deleteProject(request=request, db=db)
        except Exception as e:
            pass

        return status.HTTP_200_OK, \
               ResponseDeleteProject(
                   name=request.name,
                   error_detail=""
               )

    def getProject(self, namespace: str, db) -> (int, ResponseGetProject):
        """프로젝트 조회"""

        try:
            result = project_crud.getProject(namespace=namespace, db=db)
        except Exception as e:
            log.error(f"[프로젝트 조회 오류] {namespace} 조회 실패 -> 데이터베이스 오류: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   ResponseGetProject(
                       id=-1,
                       name=namespace,
                       error_detail="프로젝트 조회를 실패했습니다."
                   )

        if result.rowcount != 1:
            log.error(f"[프로젝트 조회 실패] 단일건 조회({namespace})지만 2개 이상 조회 되었습니다")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   ResponseGetProject(
                       id=-1,
                       name=namespace,
                       error_detail="프로젝트 조회를 실패했습니다"
                   )

        searched_project = {}
        for row in result:
            searched_project = dict(row)

        return status.HTTP_200_OK, \
               ResponseGetProject(
                   id=searched_project["id"],
                   name=searched_project["name"],
                   error_detail=""
               )

    def createProjectValid(self, namespace: str) -> bool:
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
