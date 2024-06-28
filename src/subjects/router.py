from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_session

from .models import Subject
from .schemas import PublicSubjectSchema, SubjectSchema

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
