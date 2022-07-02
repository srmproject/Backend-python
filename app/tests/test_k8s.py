from module import k8s


def test_generate_env_template():
    """env 생성"""
    jcp_k8s = k8s.JCPK8S()
    test_env = {"name": "1", "value": "2"}

    k8s_env = jcp_k8s.generate_env_template(
        name=test_env["name"],
        value=test_env["value"]
    )

    assert k8s_env.name == test_env["name"]
    assert k8s_env.value == test_env["value"]

def test_generate_envs_template():
    """env 리스트 생성"""
    jcp_k8s = k8s.JCPK8S()

    test1_env = {"name": "FILEPATH", "value": "jobs/sample/error.sh"}
    test2_env = {"name": "GIT_BRANCH", "value": "main"}
    test_envs = [test1_env, test2_env]

    k8s_envs = []
    for test_env in test_envs:
        k8s_env = jcp_k8s.generate_env_template(
            test_env["name"], test_env["value"]
        )
        k8s_envs.append(k8s_env)

    assert len(test_envs) == len(k8s_envs)
    for idx, value in enumerate(test_envs):
        assert k8s_envs[idx].name == test_envs[idx]["name"]
        assert k8s_envs[idx].value == test_envs[idx]["value"]

def test_create_job():
    """job 생성"""
    jcp_k8s = k8s.JCPK8S()

    namespace = "default"
    job_name = "jcp-k8s-jobtest-1"

    env_filepath = {"name": "FILEPATH", "value": "jobs/sample/error.sh"}
    env_giturl = {"name": "GIT_URL", "value": "https://github.com/srmproject/docker_images.git"}
    env_gitbranch = {"name": "GIT_BRANCH", "value": "main"}
    envs = [env_filepath, env_giturl, env_gitbranch]

    k8s_envs = []
    for env in envs:
        k8s_envs.append(
            jcp_k8s.generate_env_template(
                name=env["name"],
                value=env["value"]
            )
        )
    for idx, value in enumerate(k8s_envs):
        assert k8s_envs[idx].name == envs[idx]["name"]
        assert k8s_envs[idx].value == envs[idx]["value"]

    image = "busybox"
    container_template = jcp_k8s.generate_container_template(
        name=job_name,
        image=image,
        envs=k8s_envs
    )
    assert container_template.name == job_name
    assert container_template.image == image
    assert container_template.env == k8s_envs

    pod_template = jcp_k8s.generate_pod_template(
        name=job_name,
        containers=container_template,
    )
    assert pod_template.metadata.name == job_name
    assert pod_template.metadata.namespace is None

    job_template = jcp_k8s.create_job_template(
        namespace=namespace,
        job_name=job_name,
        pod_template=pod_template
    )

    assert job_template.metadata.name == job_name
    assert job_template.metadata.namespace == namespace
    assert job_template.spec.template == pod_template

    # create job
    jcp_k8s.create_job(namespace=namespace, job_template=job_template)
