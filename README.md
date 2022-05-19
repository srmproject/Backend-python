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