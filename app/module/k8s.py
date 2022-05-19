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
        log.info(f"namespace {name} 생성 시작")
        try:
            self.v1.create_namespace(ns)
            log.info("namespace 생성 성공")
        except ApiException as e:
            if e.status == 409:
                log.error(f"[-] namespace {name} 생성 중복오류")
            log.error(f"[-] namespace {name} 생성 기타 api오류: {e.status}")
        except Exception as e:
            log.error(f"[-]namespace {name} 생성 기타오류: {e}")
