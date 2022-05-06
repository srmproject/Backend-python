from database import Base
from sqlalchemy import String, Integer, Column
from domain.db_mixins import TimeStamp


class Project(TimeStamp, Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255))

    def __repr__(self) -> str:
        return f"<Project name={self.name} description={self.description}"