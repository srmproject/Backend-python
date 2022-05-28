from kubernetes import client, config
from config import cnf


class JCPK8S:
    def __init__(self):
        if cnf.ENV_STATE == "local":
            config.load_kube_config()
        
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
