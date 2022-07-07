import pytest
from module.github import JCPGithub
from fastapi import HTTPException


def test_get_branches():
    """브랜치 목록 조회"""

    github_url = "https://github.com/srmproject/docker_images.git"
    jcp_github = JCPGithub()

    branches = jcp_github.get_branches(github_url)

    assert len(branches) == 1
    assert branches[0] == "main"

def test_get_branches_failed():
    """존재하지 않는 github repo 브랜치 목록 조회"""

    github_url = "https://github.com/sdfdsfsdf/sdfsdfewwerewrsdf.git"
    jcp_github = JCPGithub()

    with pytest.raises(HTTPException):
        jcp_github.get_branches(github_url)

def test_extract_owner_and_repo():
    """github_url 추출"""

    github_url = "https://github.com/srmproject/docker_images.git"
    jcp_github = JCPGithub()

    owner, repo = jcp_github.extract_owner_and_repo(github_url)
    assert owner == "srmproject"
    assert repo == "docker_images"

# def test_get_contents():
#     jcp_github = JCPGithub()
#     repo_url = "https://github.com/choisungwook/python_pytest_practice.git"
#
#     jcp_github.get_contents(repo_url=repo_url)
