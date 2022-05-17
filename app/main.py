from fastapi import FastAPI
from config import cnf
from api.project import router as project_router
from logger import getLogger


app = FastAPI()
app.include_router(project_router)
log = getLogger()

@app.get("/")
def read_root():
    log.info(cnf.POSTGRESQL_HOST)
    log.info(cnf.POSTGRESQL_USER)
    log.info(cnf.POSTGRESQL_PASSWORD)
    return {"Hello": "World"}
