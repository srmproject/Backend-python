from module.k8s import JCPK8S
from domain.job import (
    schemas,
    crud
)
from domain.project.service import ProjectManager
from config import cnf
from logger import log
from fastapi import status, HTTPException
from module.error_code import ErrorCode
import json
from sqlalchemy import exc


class JobManager:
    def __init__(self):
        self.jcp_k8s = JCPK8S()
        self.jcp_project_manager = ProjectManager()

    def create_job(self, request: schemas.RequestCreateJob, db):
        """job 생성"""

        self.validation_or_raise_when_failed(request, db)
        self.create_job_or_raise_when_failed(db, request)

    def create_job_or_raise_when_failed(self, db, request):
        """job 생성(실패시 http exception 예외 발생)"""

        try:
            crud.create_job(request=request, db=db)
        except exc.IntegrityError as sqlalchemy_error:
            error_msg = "job[{}] 생성을 실패했습니다[에러코드: {}]. 관리자에게 문의하세요".format(
                request.job_name,
                ErrorCode.CREATE_JOB_DB_ERROR
            )
            log.error(f"{error_msg}. 에러 상세메시지->{sqlalchemy_error} 상세정보->{json.dumps(request.dict())}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error_msg": error_msg}
            )

    def get_jobs(self, db):
        """job 전체조회"""

        rows = crud.get_jobs(db)
        jobs = [dict(row) for row in rows]

        return jobs

    def get_project_from_projectid(self, project_id: str, db):
        """project_id로 프로젝트 조회"""

        return self.jcp_project_manager.get_project_from_projectid(project_id=project_id, db=db)

    def execute_job(self):
        """job 실행"""

        # # job 템플릿 생성
        # envs = self.generate_conatiner_envs(request)
        # container_template = self.generate_container_template(envs, request)
        # pod_template = self.generate_pod_template(container_template, request)
        # job_template = self.generate_job_template(pod_template, request)
        # try:
        #     self.jcp_k8s.execute_job(
        #         namespace=request.project_name,
        #         job_template=job_template
        #     )
        # except Exception as e:
        #     log.error(f"[error] job 실행 오류: {e}")
        pass

    def generate_job_template(self, pod_template, request):
        """job template 생성"""

        return self.jcp_k8s.create_job_template(
            namespace=request.project_name,
            job_name=request.job_name,
            pod_template=pod_template
        )

    def validation_or_raise_when_failed(self, request: schemas.RequestCreateJob, db):
        """유효성 검사(실패시 http exception 예외 발생)"""

        # 이름에 "_"가 있는지 검사
        if "_" in request.job_name:
            error_msg = "job[{}] 이름에 '_'가 포함되면 안됩니다. 다시 입력하세요".format(
                request.job_name,
                ErrorCode.CREATE_JOB_VALIDATION_NAME_IS_NOT_EXIST
            )
            log.error(f"{error_msg}. 상세정보->{json.dumps(request.dict())}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_msg": error_msg}
            )

        # 프로젝트가 없음
        project = self.get_project_from_projectid(project_id=request.project_id, db=db)
        if not project:
            error_msg = "프로젝트가 존재하지 않습니다[에러코드: {}]. 관리자에게 문의하세요".format(
                ErrorCode.CREATE_JOB_VALIDATION_PROJECT_IS_NOT_EXIST
            )
            log.error(f"{error_msg}. 상세정보->{json.dumps(request.dict())}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error_msg": error_msg}
            )

        # 쿠버네티스 namespace가 없음
        if not self.jcp_k8s.is_exist_namespace(project["name"]):
            error_msg = "job[{}] 생성을 실패했습니다[에러코드: {}]. 관리자에게 문의하세요".format(
                request.job_name,
                ErrorCode.CREATE_JOB_VALIDATION_NAMESPACE_IS_NOT_EXIST
            )

            log.error(f"{error_msg}. 상세정보->{json.dumps(request.dict())}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error_msg": error_msg}
            )

    def generate_pod_template(self, container_template, request):
        """pod 템플릿 생성"""

        return self.jcp_k8s.generate_pod_template(
            name=request.job_name,
            containers=container_template
        )

    def generate_container_template(self, envs, request):
        """컨테이너 템플릿 생성"""

        return self.jcp_k8s.generate_container_template(
            name=request.job_name,
            image=self.get_image(),
            envs=envs
        )

    def get_image(self):
        """이미지 조회"""

        if cnf.ENV_STATE == "local":
            return "choisunguk/jcp_job:v1"

        return "192.168.0.66:31831/jobs_shell:alpha"

    def generate_conatiner_envs(self, request):
        """container.spec.env 생성"""

        env_giturl = {"name": "GIT_URL", "value": request.github.url}
        env_gitbranch = {"name": "GIT_BRANCH", "value": request.github.branch}
        env_filepath = {"name": "FILEPATH", "value": request.github.runfile}
        envs = [env_giturl, env_gitbranch, env_filepath]

        k8s_envs = []
        for env in envs:
            k8s_envs.append(
                self.jcp_k8s.generate_env_template(
                    name=env["name"],
                    value=env["value"]
                )
            )

        return k8s_envs
