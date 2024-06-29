from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session

from .models import Subject
from .schemas import PublicSubjectSchema, SubjectList, SubjectSchema

Session = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix='/api/v1/subjects', tags=['subjects'])


@router.post(
    '/', response_model=PublicSubjectSchema, status_code=HTTPStatus.CREATED
)
def create_subject(
    subject: SubjectSchema,
    session: Session,  # type: ignore
):
    db_subject = Subject(subject.name, updated_at=datetime.now())

    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)

    return db_subject


@router.get('/', response_model=SubjectList, status_code=HTTPStatus.OK)
def list_subjects(session: Session):  # type: ignore
    subjects = session.scalars(select(Subject)).all()

    return {'subjects': subjects}
