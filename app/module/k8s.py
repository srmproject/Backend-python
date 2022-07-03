from kubernetes import client, config
from config import cnf
from logger import log
from typing import Union


class JCPK8S:
    def __init__(self):
        log.info("[*][*] 쿠버네티스 설정 로드 시작")
        if cnf.ENV_STATE == "local":
            log.info("[*][*] local 설정 로드")
            config.load_kube_config()
        elif cnf.ENV_STATE == "dev":
            log.info("[*][*] dev 설정 로드")
            config.load_incluster_config()

    def create_namespace(self, namespace) -> None:
        """namespace 생성"""

        v1 = client.CoreV1Api()
        ns = client.V1Namespace()
        ns.metadata = client.V1ObjectMeta(name=namespace)
        v1.create_namespace(ns)

    def delete_namespace(self, namespace) -> None:
        """namespace 삭제"""

        v1 = client.CoreV1Api()
        v1.delete_namespace(namespace)

    def is_exist_namespace(self, namespace):
        """namespace 존재확인"""

        v1 = client.CoreV1Api()
        namespaces = v1.list_namespace()

        for item in namespaces.items:
            if item.metadata.name == namespace:
                return True

        return False

    def generate_container_template(self, name, image, envs=None, args=None, command=None) -> client.V1Container:
        """컨테이너 템플릿 생성"""

        return client.V1Container(
            name=name,
            image=image,
            image_pull_policy="Always",
            env=envs,
            args=args,
            command=command
        )

    def generate_env_template(self, name: str, value: str):
        """env템플릿 생성"""

        return client.V1EnvVar(
            name=name,
            value=value,
        )

    def generate_pod_template(self, name: str, containers, namespace: Union[str, None]=None) -> client.V1PodTemplateSpec:
        """
        pod 템플릿 생성
        :param name:
        :param namespace:
        :return:
        """

        return client.V1PodTemplateSpec(
            spec=client.V1PodSpec(restart_policy="Never", containers=[containers]),
            metadata=client.V1ObjectMeta(name=name, namespace=namespace, labels={"app": name}),
        )

    def create_job_template(self, namespace: str, job_name: str, pod_template: client.V1PodTemplateSpec):
        """
        job 생성

        :param namespace: namespace 이름
        :param job_name: job 이름
        :return:
        """

        metadata = client.V1ObjectMeta(
            name=job_name,
            namespace=namespace,
            labels={"app": job_name}
        )
        spec = client.V1JobSpec(
            backoff_limit=0,
            template=pod_template
        )

        return client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=metadata,
            spec=spec
        )

    def execute_job(self, namespace, job_template) -> client.V1Job:
        """job 실행"""

        batch_api = client.BatchV1Api()
        return batch_api.create_namespaced_job(namespace, job_template)
