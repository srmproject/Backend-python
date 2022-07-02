from module import k8s
from kubernetes import client, config

# def test_create_namespace():
#     jcp_k8s = k8s.JCPK8S()
#
#     namespace = "jcp-k8s-test1"
#     jcp_k8s.createNamespace(namespace=namespace)


def test_create_job():
    """job 생성"""
    jcp_k8s = k8s.JCPK8S()

    namespace = "default"
    job_name = "jcp-k8s-jobtest-1"

    container_template = jcp_k8s.generate_container_template(name=job_name, image="busybox")
    pod_template = jcp_k8s.generatePodTemplate(
        name=job_name,
        namespace=namespace,
        containers=container_template,
    )

    job_template = jcp_k8s.create_job_template(
        namespace=namespace,
        job_name=job_name,
        pod_template=pod_template
    )

    created_job_obj = jcp_k8s.create_job(namespace=namespace, job_template=job_template)
