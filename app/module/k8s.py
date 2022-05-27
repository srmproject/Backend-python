from kubernetes import client, config
from config import cnf
from logger import log
from kubernetes.client.exceptions import ApiException


class JCPK8S:
    def __init__(self):
        if cnf.ENV_STATE == "local":
            config.load_kube_config()
        
        self.v1 = client.CoreV1Api()
        
    def createNamspace(self, name):
        '''
        namespace생성
        
        :params
          name: namespace 이름
        '''
        ns = client.V1Namespace()
        ns.metadata = client.V1ObjectMeta(name=name)
        self.v1.create_namespace(ns)
