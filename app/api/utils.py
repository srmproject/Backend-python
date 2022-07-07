from fastapi import APIRouter, status
from logger import log
from module.github import JCPGithub
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/api/v1",
    tags=["utils"]
)

@router.get("/utils/git/branches")
def get_git_branches(github_url: str):
    """git branch 목록 조회"""

    log.info("============ get_git_branches get called =============")
    log.info(f"url->{github_url}")
    jcp_github = JCPGithub()
    branches = jcp_github.get_branches(github_url)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "branches": branches
        }
    )
