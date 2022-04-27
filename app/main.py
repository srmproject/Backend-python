from fastapi import FastAPI
from config import cnf

app = FastAPI()

@app.get("/")
def read_root():
    print(cnf.POSTGRESQL_HOST)
    print(cnf.POSTGRESQL_USER)
    print(cnf.POSTGRESQL_PASSWORD)
    return {"Hello": "World"}
