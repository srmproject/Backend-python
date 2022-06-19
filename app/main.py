from fastapi import FastAPI
from config import cnf
from api.project import router as project_router
from logger import log
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(project_router)

@app.get("/")
def read_root():
    log.info(cnf.POSTGRESQL_HOST)
    log.info(cnf.POSTGRESQL_USER)
    log.info(cnf.POSTGRESQL_PASSWORD)
    return {"Hello": "World"}
