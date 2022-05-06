from database import Base, engine
from domain.project.models import Project


if __name__=="__main__":
    print("Creating database ...")
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"[-] Error create database: {e}")
