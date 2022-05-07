from sqlalchemy.orm import Session
from domain.project.schemas import ProjectCreate, ProjectSchema
from domain.project.models import Project


def createProject(project: ProjectCreate, db: Session):
    '''프로젝트 생성'''
    new_project = Project(
        name=project.name,
        description=project.description
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return ProjectSchema.from_orm(new_project)
