from http import HTTPStatus

from fastapi import APIRouter
from sqlalchemy import select

from src.database import T_Session

from .models import Subject
from .schemas import PublicSubjectSchema, SubjectList, SubjectSchema
from .service import SubjectService

router = APIRouter(prefix='/api/v1/subjects', tags=['subjects'])


@router.post(
    '/', response_model=PublicSubjectSchema, status_code=HTTPStatus.CREATED
)
def create_subject(
    subject: SubjectSchema,
    session: T_Session,
):
    db_subject = SubjectService.post(session, subject)
    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)

    return db_subject


@router.get('/', response_model=SubjectList, status_code=HTTPStatus.OK)
def list_subjects(session: T_Session):
    subjects = session.scalars(select(Subject)).all()

    return {'subjects': subjects}


@router.put(
    '/{subject_id}',
    response_model=PublicSubjectSchema,
    status_code=HTTPStatus.OK,
)
def update_subject(
    subject_id: int,
    subject: SubjectSchema,
    session: T_Session,
):
    db_subject = SubjectService.put(session, subject, subject_id)
    session.commit()
    session.refresh(db_subject)

    return db_subject


@router.delete('/{subject_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_subject(subject_id: int, session: T_Session):  # type: ignore
    db_subject = SubjectService.delete(session, subject_id)

    session.delete(db_subject)
    session.commit()
