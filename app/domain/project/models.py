from database import Base
from sqlalchemy import String, Integer, Column


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True, unique=True)
    description = Column(String(255))

    def __repr__(self) -> str:
        return f"<Project name={self.name} description={self.description}"