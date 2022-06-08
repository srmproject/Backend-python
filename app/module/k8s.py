from kubernetes import client, config
from config import cnf
from logger import log


class JCPK8S:
    def __init__(self):
        log.info("[*][*] 쿠버네티스 설정 로드 시작")
        if cnf.ENV_STATE == "local":
            log.info("[*][*] local 설정 로드")
            config.load_kube_config()
        elif cnf.ENV_STATE == "dev":
            log.info("[*][*] dev 설정 로드")
            config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        
    def createNamespace(self, namespace) -> None:
        """
        namespace 생성

        :param
          namespace: namespace 이름
        """
        ns = client.V1Namespace()
        ns.metadata = client.V1ObjectMeta(name=namespace)
        self.v1.create_namespace(ns)

    def deleteNamespace(self, namespace) -> None:
        """
        namespace 삭제

        :param
          namespace: namespace 이름
        :return:
        """
        ns = client.V1Namespace()
        self.v1.delete_namespace(namespace)
