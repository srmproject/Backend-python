from fastapi import status
from kubernetes.client.exceptions import ApiException
from domain.project import schemas
import domain.project.crud as project_crud
from logger import log
from module.k8s import JCPK8S


class ProjectManager:
    def createProject(self, request: schemas.RequestCreateProject, db) -> (int, schemas.ResponseCreateProject):
        """프로젝트 생성"""
        k8s = JCPK8S()
        log.info("[*] 프로젝트 생성 시작")

        log.info("[*] 프로젝트 유효성검사 시작")
        if not self.createProjectValid(request=request, db=db):
            return status.HTTP_401_UNAUTHORIZED, \
                   schemas.ResponseCreateProject(
                       user_id=request.user_id,
                       project_name=request.project_name,
                       error_detail=f"user_id {request.user_id}가 존재하지 않습니다."
                   )
        log.info("[*] 프로젝트 유효성검사 종료")

        # 쿠버네티스 namespace 생성
        try:
            log.info("[*] 쿠버네티스 namespace 생성 시작")
            k8s.createNamespace(namespace=request.project_name)
            log.info("[*] 쿠버네티스 namespace 생성 종료")
        except ApiException as e:
            if e.status == 409:
                log.error(f"[프로젝트 생성 오류] k8s namespace {request.project_name}이 이미 존재합니다")
                return status.HTTP_409_CONFLICT, \
                       schemas.ResponseCreateProject(
                           user_id=request.user_id,
                           project_name=request.project_name,
                           error_detail=f"{request.project_name}이 이미 존재합니다."
                       )

            log.error(f"[프로젝트 생성 오류] k8s namespace {request.project_name} 기타 생성오류: {e.status}. {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   schemas.ResponseCreateProject(
                       user_id=request.user_id,
                       project_name=request.project_name,
                       error_detail=str(e)
                   )

        # github repo 생성
        # createRepo(repo_name=request.name, token=request.github_token)

        # db 업데이트
        try:
            log.info("[*] 프로젝트 DB 등록 시작")
            project_crud.createProject(request=request, db=db)
            log.info("[*] 프로젝트 DB 등록 종료")
        except Exception as e:
            db_error_code = e.args[0].orig.pgcode
            if db_error_code == "23503":
                log.error(f"[프로젝트 생성 오류] 데이터베이스 오류: user_id가 존재하지 않음 {db_error_code}->{e}")
            else:
                log.error(f"[프로젝트 생성 오류] 데이터베이스 오류: 기타에러 {e.args[0].code}->{e}")

            # 생성했던 쿠버네티스 네임스페이스 삭제
            try:
                k8s.deleteNamespace(namespace=request.project_name)
            except Exception:
                pass

            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   schemas.ResponseCreateProject(
                       user_id=request.user_id,
                       project_name=request.project_name,
                       error_detail="프로젝트 생성을 실패했습니다."
                   )

        return status.HTTP_201_CREATED, \
               schemas.ResponseCreateProject(
                   user_id=request.user_id,
                   name=request.project_name,
                   error_detail=""
               )

    def deleteProject(self, request: schemas.RequestDeleteProject, db) -> (int, schemas.ResponseDeleteProject):
        """프로젝트 삭제"""
        k8s = JCPK8S()

        # 유저 확인
        if not self.isExistDBUser(user_id=request.user_id, db=db):
            return status.HTTP_401_UNAUTHORIZED, \
                   schemas.ResponseDeleteProject(
                       user_id=request.user_id,
                       project_name=request.project_name,
                       error_detail=f"user_id {request.user_id}가 존재하지 않습니다."
                   )

        # 쿠버네티스 네임스페이스 삭제
        try:
            k8s.deleteNamespace(namespace=request.project_name)
        except ApiException as e:
            pass

        # DB행 삭제
        try:
            project_crud.deleteProject(request=request, db=db)
        except Exception as e:
            pass

        return status.HTTP_200_OK, \
               schemas.ResponseDeleteProject(
                   user_id=request.user_id,
                   project_name=request.project_name,
                   error_detail=""
               )

    def getProject(self, request: schemas.RequestGetProject, db) -> (int, schemas.ResponseGetProject):
        """프로젝트 단일조회"""
        # 유저 확인
        if not self.isExistDBUser(user_id=request.user_id, db=db):
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   schemas.ResponseGetProject(
                       project_id=-1,
                       user_id=request.user_id,
                       project_name=request.project_name,
                       error_detail=f"user_id {request.user_id}가 존재하지 않습니다."
                   )

        try:
            result = project_crud.getProject(request=request, db=db)
        except Exception as e:
            log.error(f"[프로젝트 조회 오류] {request.project_name} 조회 실패 -> 데이터베이스 오류: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   schemas.ResponseGetProject(
                       project_id=-1,
                       user_id=request.user_id,
                       project_name=request.project_name,
                       error_detail="데이터베이스 오류로 프로젝트 조회를 실패했습니다."
                   )


        if result.rowcount == 0:
            log.error(f"[프로젝트 조회 실패] 프로젝트({request.project_name})가 존재하지 않습니다.")
            return status.HTTP_404_NOT_FOUND, \
                   schemas.ResponseGetProject(
                       project_id=-1,
                       user_id=request.user_id,
                       project_name=request.project_name,
                       error_detail=f"{request.project_name}프로젝트가 존재하지 않습니다."
                   )

        project = {}
        for row in result:
            project = dict(row)

        return status.HTTP_200_OK, \
               schemas.ResponseGetProject(
                   project_id=project["id"],
                   user_id=project["user_id"],
                   project_name=project["name"],
                   error_detail=""
               )

    def getProjects(self, user_id: str, db) -> (int, schemas.ResponseGetProjects):
        """프로젝트 전체조회"""
        # 유저 확인
        if not self.isExistDBUser(user_id=user_id, db=db):
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   schemas.ResponseGetProjects(
                       results=[],
                       error_detail=f"user_id {user_id}가 존재하지 않습니다."
                   )
        try:
            rows = project_crud.getProjects(db=db)
        except Exception as e:
            log.error(f"[프로젝트 전체 조회 오류] 조회 실패 -> 데이터베이스 오류: {e}")
            return status.HTTP_500_INTERNAL_SERVER_ERROR, \
                   schemas.ResponseGetProjects(
                       results=[],
                       error_detail="프로젝트 조회를 실패했습니다."
                   )

        projects = []
        for row in rows:
            project = dict(row)
            projects.append(
                schemas.ProjectInfo(
                    project_id=project["id"],
                    user_id=project["user_id"],
                    project_name=project["name"]
                )
            )

        return status.HTTP_200_OK, \
               schemas.ResponseGetProjects(
                   results=projects,
                   error_detail=""
               )

    def createProjectValid(self, request: schemas.RequestCreateProject, db) -> bool:
        """
        프로젝트 생성 유효성 검사
          ① k8s namespace 확인

        :params
          request: 프로젝트 생성 요청

        :return
          bool
            True: 유효성 검사 성공
            False: 유효성 검사 실패
        """
        return self.isExistK8sNamespace(namespace=request.project_name) \
               and self.isExistDBUser(user_id=request.user_id, db=db)

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

    def isExistDBUser(self, user_id: str, db) -> bool:
        """
        데이터베이스에 user가 존재하는지 확인
        :param user_id:
        :return:
        """
        rows = project_crud.getUser(user_id=user_id, db=db)
        if rows.rowcount == 0:
            log.error(f"user {user_id}가 존재하지 않습니다.")
            return False

        return True
