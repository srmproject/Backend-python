from fastapi import FastAPI
from config import cnf
from api.project import router as project_router

app = FastAPI()
app.include_router(project_router)

@app.get("/")
def read_root():
    print(cnf.POSTGRESQL_HOST)
    print(cnf.POSTGRESQL_USER)
    print(cnf.POSTGRESQL_PASSWORD)
    return {"Hello": "World"}
