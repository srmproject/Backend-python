# 개요
* 파이썬으로 개발된 파이썬

# 준비
* postgresql
```sh
docker run --name=postegresql -d \
-p 5432:5432 \
-e POSTGRES_USER=root \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=jcp \
postgres:12-alpine
```

* kubernetes serviceaccount
```sh
kubectl create ns jcp
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin
  namespace: jcp
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin
  namespace: jcp
```