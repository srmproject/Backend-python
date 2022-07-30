from github import Github
from fastapi import HTTPException, status
import requests
from module.error_code import ErrorCode
from logger import log


def createRepo(repo_name: str, token: str):
    """repo 생성"""
    g = Github(token)
    user = g.get_user()
    user.create_repo(repo_name)


class JCPGithub:
    def __init__(self):
        self.endpoint = "https://api.github.com"

    def get_contents(self, repo_url: str):
        """github 컨텐츠(파일, 디렉터리) 조회"""

        raise NotImplementedError
        # if not re.match(r"{self.endpoint}/[A-Za-z\d_-]/?", repo_url):
        #     raise HTTPException(
        #         status_code=400,
        #         detail={"msg": "url이 올바르지 않습니다. 다시 확인해주세요"},
        #     )
        #
        # converted_url = self.convert_repo_url(repo_url)

    def extract_owner_and_repo(self, github_url: str) -> (str, str):

        split_text = github_url.split("https://github.com/")

        if len(split_text) != 2:
            log.error("[-] extract github url is failed")
            raise RuntimeError

        owner_repo_text = split_text[1]
        owner = owner_repo_text.split("/")[0]
        repo = owner_repo_text.split("/")[1].replace(".git", "")

        return owner, repo

    def validation_github_url(self, github_url: str):
        """github url 유효성 검사"""

        if not github_url.startswith("https://github.com"):
            error_msg = "[Error code {}] github url는 https://github.com로 시작해야 합니다.".format(
                ErrorCode.CREATE_JOB_VALIDATION_GITHUB_URL_INCORRECT_PREFIX
            )
            log.error(f"{error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_msg": error_msg}
            )

        if not github_url.endswith(".git"):
            error_msg = "[Error code {}] github은 .git으로 끝나야 합니다".format(
                ErrorCode.CREATE_JOB_VALIDATION_GITHUB_URL_INCORRECT_POSTFIX
            )
            log.error(f"{error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error_msg": error_msg}
            )

    def get_branches(self, github_url: str):
        """브랜치 목록 조회"""

        self.validation_github_url(github_url)

        owner, repo = self.extract_owner_and_repo(github_url)
        headers = {
            "Accept": "application/vnd.github+json"
        }
        url = f"{self.endpoint}/repos/{owner}/{repo}/branches"
        response = requests.get(url, headers=headers)

        if not response.ok:
            self.get_branch_error_handling(response)

        return [item.get("name") for item in response.json()]

    def get_branch_error_handling(self, response):
        """브랜치 목록 조회 실패 에러 핸들링"""

        if response.status_code == status.HTTP_404_NOT_FOUND:
            error_msg = "[Error code {}] github_url이 존재하지 않습니다. 다시 입력하세요".format(
                ErrorCode.CREATE_JOB_VALIDATION_GITHUB_URL_IS_NOT_EXIST
            )
            log.error(f"{error_msg}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error_msg": error_msg}
            )
        log.error(f"[-] get branch list is failed. other exception-> {response.text}")
        error_msg = "[Error code {}] 브랜치 조회 오류가 발생했습니다. 수동으로 입력해주세요".format(
            ErrorCode.CREATE_JOB_VALIDATION_GET_BRANCH_OTHER_EXCEPTION
        )
        log.error(f"{error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_msg": error_msg}
        )
