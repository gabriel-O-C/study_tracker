from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from src.database import T_Session

from .models import Subject
from .schemas import SubjectSchema


def create_subject(session: T_Session, subject: SubjectSchema):
    db_subject = session.scalar(
        select(Subject).where(Subject.name == subject.name)
    )

    if db_subject:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Subject already exists'
        )

    db_subject = Subject(subject.name, updated_at=datetime.now())

    return db_subject
